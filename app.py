# app.py - Updated with Sales & Billing
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import date

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL Config (Update password if needed)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ABC_PLSCHANGETHIS',  # CHANGE THIS
    'database': 'pharmacy_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Database Error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        flash("Cannot connect to database!")
        return render_template('index.html', medicines=[])
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicines ORDER BY name")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', medicines=medicines)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        manufacturer = request.form['manufacturer']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        expiry = request.form['expiry']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (name, manufacturer, price, quantity, expiry_date) VALUES (%s, %s, %s, %s, %s)",
                       (name, manufacturer, price, quantity, expiry))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Medicine added!")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        manufacturer = request.form['manufacturer']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        expiry = request.form['expiry']
        cursor.execute("UPDATE medicines SET name=%s, manufacturer=%s, price=%s, quantity=%s, expiry_date=%s WHERE id=%s",
                       (name, manufacturer, price, quantity, expiry, id))
        conn.commit()
        flash("Updated!")
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM medicines WHERE id=%s", (id,))
    medicine = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', medicine=medicine)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Deleted!")
    return redirect(url_for('index'))

# NEW: Sales Routes
@app.route('/sales')
def sales_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id, s.quantity_sold, s.sale_date, s.total_amount, m.name as medicine_name, m.price
        FROM sales s JOIN medicines m ON s.medicine_id = m.id
        ORDER BY s.sale_date DESC
    """)
    sales = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sales.html', sales=sales)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicines WHERE quantity > 0 ORDER BY name")
    medicines = cursor.fetchall()
    cursor.close()

    # Always define today for the template
    today = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        med_id = int(request.form['medicine_id'])
        qty_sold = int(request.form['quantity_sold'])
        sale_date = request.form['sale_date']

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT price, quantity FROM medicines WHERE id = %s", (med_id,))
        med = cursor.fetchone()
        cursor.close()

        if not med or qty_sold > med['quantity']:
            flash("Not enough stock!")
            conn.close()
            return render_template('sell.html', medicines=medicines, today=today)

        total = qty_sold * med['price']

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sales (medicine_id, quantity_sold, sale_date, total_amount)
            VALUES (%s, %s, %s, %s)
        """, (med_id, qty_sold, sale_date, total))
        sale_id = cursor.lastrowid

        cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (qty_sold, med_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Sale recorded! Total: ₹{total:.2f}")
        return redirect(url_for('receipt', sale_id=sale_id))

    conn.close()
    return render_template('sell.html', medicines=medicines, today=today)    
   

@app.route('/receipt/<int:sale_id>')
def receipt(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, m.name as medicine_name
        FROM sales s JOIN medicines m ON s.medicine_id = m.id
        WHERE s.id = %s
    """, (sale_id,))
    sale = cursor.fetchone()
    cursor.close()
    conn.close()
    if not sale:
        flash("Sale not found!")
        return redirect(url_for('sales_list'))
    return render_template('receipt.html', sale=sale)

if __name__ == '__main__':
    app.run(debug=True)
