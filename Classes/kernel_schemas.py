#Schemas Manager
import os
import sqlparse
from bintrees import FastRBTree
from kernel_attributes import kernel_attributes
import pickle

class kernel_schemas:
    def __init__(self,db_name):
        self.db_name="../DataBases/"+db_name+".dat"
        self.schemas=FastRBTree()
    def append_schema(self,attributes,name):
        schema=kernel_attributes(name,attributes)
        print(self.db_name)
        try:
            with open(self.db_name,"ab") as fil:
               pickle.dump(schema, fil)
            print("Schema ",schema.name," created succesfully")
        except Exception as e:
            print("Error: File doesn't exist or it is corrupted")
    def read_schema(self):
        try:
            with open(self.db_name,"rb") as fil:
                while True:
                    try:
                       obj=pickle.load(fil)
                       name=obj.name
                       self.schemas[name]=obj
                       print("Schema ",name," charged succsefully")
                    except EOFError:
                      break
        except Exception as e:
            print(f"Error: {e}")
        
            
            
    def get_schema(self,name):
        print(self.schemas[name])
        
        
    