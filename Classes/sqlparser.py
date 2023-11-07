#Parse class
import sqlparse 
import os
from Attributes import attribute
from kernel_databases import kernel_databases
import re

class parser:
    def __init__(self,query):
        self.query=query
        self.parsed=sqlparse.parse(self.query)
    def QUERY(self,db_name):
        statement=self.parsed[0]
        if statement.get_type()=="CREATE":
            self.CREATE(statement,db_name)
        if statement.get_type()=="INSERT":
            self.INSERT(statement,db_name)
    def CREATE(self,statement,db_name):
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        attributes=self.TransformsC(attributes)
        atr=[]
        for i in range(1,len(attributes),2):
            Attribute=attribute(attributes[i-1],attributes[i])
            atr.append(Attribute)
        db=kernel_databases()
        db.append_schema(atr,name,db_name)
    def INSERT(self,statement,db_name):
        return 0
            
    def TransformsC(self,attributes):
        attributes=re.split(r'[, ]',str(attributes))
        attributes[0]=attributes[0].replace("(","")
        attributes[len(attributes)-1]=attributes[len(attributes)-1].replace(")","")
        return attributes
        
            
        
        
       
        