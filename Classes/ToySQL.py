#Main Class
import os
from Database import Database
from sqlparser import parser
from kernel_schemas import kernel_schemas
#Main functions
#Please, to use first change to the folder classes with comand "cd classes" and try to run 
def switch_case(opcion):
    while opcion!="3":
        print("Options of DBMS: ")
        print("1-'Create database'     2-'Enter on a database'  3-'Power off'" )
        opcion=input("Select an option: ")
        if opcion == "1":
           db=Database()
           name=input("Name: ")
           db.create(name)
        elif opcion == "2":
            db_name=input("Name of database: ")
            db=kernel_schemas(db_name)
            op="2"
            val=db.read_schema()
            if val!=None:
                op="1"
            while op!="2":
                print("Options of DBMS: ")
                print("1-'Query'     2-'Back' " )
                op=input("Select an option: ")
                if op=="1":
                    query=input("Query: ")
                    p=parser(query,db)
                    p.QUERY()   
                elif op!="1" and op!="2":
                    print("Invalid option")
        elif opcion=="3":
            print("ToySQL Finished, thanks for using >.<")
        else:
            if opcion=="3":
               print("ToySQL Finished, thanks for using >.<")
            else:
               print("no valid option")

op=1
switch_case(op)


