
'''
with open("one.txt","w") as file:
 st="Hello World"
 file.write(st)
print("file created") 
'''
'''

with open("two.txt","w") as file:
    st=['this line one \n','line two \n','line three \n']
    file.writelines(st)
print("success")    

'''
'''
with open("one.txt","r") as file:
 data=file.read()
print(data)
'''
with open("two.txt","r") as file:
    line_list =file.readlines()
print(line_list)
