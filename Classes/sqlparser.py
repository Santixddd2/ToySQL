#Parse class
import sqlparse 
import os
from Attributes import attribute
from kernel_schemas import kernel_schemas
import re

class parser:
    def __init__(self,query,db):
        self.db=db
        self.query=query
        self.parsed=sqlparse.parse(self.query)
    def QUERY(self):
        statement=self.parsed[0]
        if statement.get_type()=="CREATE":
            self.CREATE(statement,self.db)
        if statement.get_type()=="INSERT":
            self.INSERT(statement,self.db)
            
    def CREATE(self,statement,db):
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        attributes=self.TransformsC(attributes)
        atr=[]
        for i in range(1,len(attributes),2):
            Attribute=attribute(attributes[i-1],attributes[i])
            atr.append(Attribute)
        db.append_schema(atr,name)
        
    def INSERT(self,statement,db):
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        attributes=self.TransformsA(str(attributes))
        db.insert_data(name,attributes)
            
    def TransformsC(self,attributes):
        attributes=re.split(r'[, ]',str(attributes))
        attributes[0]=attributes[0].replace("(","")
        attributes[len(attributes)-1]=attributes[len(attributes)-1].replace(")","")
        return attributes
    def TransformsA(self,attributes):
        attributes=re.split(r'[, (]',str(attributes))
        del attributes[0]
        attributes[len(attributes)-1]=re.split(r'[, ]',attributes[len(attributes)-1])
        attributes[0]=str(attributes[0]).replace("(","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace(")","")
        attributes[0]=str(attributes[0]).replace("'","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("'","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("[","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("]","")
        return attributes
        
            
        
        
       
        