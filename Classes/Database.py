#Daatabase manager
import os
import sqlparse 
from kernel_databases import kernel_databases

class Database:
    def __init__(self):
        self.databases=[]
    def append(self,database):
        self.databases.append(database)
    def charge(self):
        return 0
    def create(self,name):
        file="../DataBases/"+name+".dat"
        with open(file, "w") as file:
            pass
        print("Database ",name," created succsefully")
    


