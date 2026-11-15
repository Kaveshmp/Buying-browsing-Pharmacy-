# Pharmacy Management System

A lightweight, Flask-based web application for managing pharmacy inventory, processing sales, and generating billing receipts. 

## Features
* **Inventory Management**: View, add, edit, and delete medicine records.
* **Stock Tracking**: Automatically deducts medicine quantities when a sale is processed.
* **Sales & Billing**: Record new sales, calculate total amounts dynamically, and view sales history.
* **Receipt Generation**: Generate digital receipts for completed transactions.
* **Secure Configuration**: Uses `.env` for database credentials and secret keys.

## Tech Stack
* **Backend**: Python, Flask
* **Database**: MySQL (`mysql-connector-python`)
* **Environment Management**: `python-dotenv`
* **Frontend**: HTML/CSS (Jinja2 Templates)

## Prerequisites
* Python 3.7+
* MySQL Server

## Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/pharmacy-management.git](https://github.com/yourusername/pharmacy-management.git)
cd pharmacy-management
