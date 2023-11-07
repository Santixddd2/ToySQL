#Schemas Manager
import os
import sqlparse
from bintrees import FastRBTree
from kernel_schemas import kernel_schemas
import pickle

class kernel_databases:
    def __init__(self):
        self.schemas=FastRBTree()
    def append_schema(self,attributes,name,db_name):
        schema=kernel_schemas(name,attributes)
        name=schema.name
        self.schemas[name]=schema
        fil="../DataBases/"+db_name+".dat"
        print(fil)
        try:
            with open(fil,"ab") as fil:
               pickle.dump(schema, fil)
            print("Schema ",schema.name," created succesfully")
        except Exception as e:
            print("Error: File doesn't exist or it is corrupted")
            
            
    def get_schema(self,name):
        print(self.schemas[name])
        
        
    