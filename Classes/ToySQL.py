#Main Class
import os
from Database import Database
from sqlparser import parser
from kernel_schemas import kernel_schemas
#Main functions
def switch_case(opcion):
    if opcion == 1:
        db=Database()
        name=input("Name: ")
        db.create(name)
    elif opcion == 2:
         db_name=input("Name of database: ")
         db=kernel_schemas(db_name)
         db.read_schema()
         print("Consult ")
         query=input("Query: ")
         p=parser(query,db)
         p.QUERY()   
    else:
        print("no valid option")

print("Options of DBMS: ")
print("1-'Create database'     2-'Enter on a database'")
op=int(input("Select an option: "))
switch_case(op)


