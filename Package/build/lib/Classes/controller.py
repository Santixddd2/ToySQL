#Controller for use on other aplications.
import os
from .Database import Database
from .sqlparser import parser
from .kernel_schemas import kernel_schemas
from .config import *
from .data import data
class DatabaseController():
    def __init__(self):
        self.db=None
    
    def open_conection(self,route,credentials):
        db=kernel_schemas(route)
        print(db)
        val=db.read_schema()
        if val==None:
           print("Error")
        else: 
           self.db=db
           print("Conection open")
    def close_conection(self):
        self.db=None
        
    def create_database(self,name,route):
        db=Database()
        db.create(name,route)
    
    def query(self,query):
        p=parser(query,self.db)
        data=p.QUERY()   
        return data
        
    
    #For later
    
    def validation(self):
        return 0

    def config(self,name,value):
        #try:
           #config.name=value
        #except:
            #print("Error with the value or name")
        return 0
    