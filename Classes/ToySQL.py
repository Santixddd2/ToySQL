#Main Class
import os
from Database import Database
from sqlparser import parser

def switch_case(opcion):
    if opcion == 1:
        db=Database()
        name=input("Name: ")
        db.create(name)
    elif opcion == 2:
         db_name=input("Name of database: ")
         print("Consult ")#Replace with SQL consults
         query=input("Query: ")
         p=parser(query)
         p.QUERY(db_name)   
    else:
        print("no valid option")

print("Options of DBMS: ")
print("1-'Create database'     2-'Enter on a database'")
op=int(input("Select an option: "))
switch_case(op)


