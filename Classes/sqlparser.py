#Parse class
import sqlparse 
import os
from Attributes import attribute
from kernel_schemas import kernel_schemas
import re
from images import image

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
        if statement.get_type()=="SELECT":
            self.SELECT(statement,self.db)
            
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
        
    def SELECT(self,statement,db):
        name=str(statement.tokens[6])
        columns=str(statement.tokens[2])
        where=str(statement.tokens[-1])
        name,dat,columns=self.TransformsCO(name,where,columns)
        #print(dat)
        db.select_data(name,dat,columns)
        
        
    #STRING TRANSFORMATIONS
    

    #Transforms for create
    def TransformsC(self,attributes):
        attributes=re.split(r'[, ]',str(attributes))
        attributes[0]=attributes[0].replace("(","")
        attributes[len(attributes)-1]=attributes[len(attributes)-1].replace(")","")
        return attributes
    #Transforms for Insert
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
    #Transforms for select
    def TransformsCO(self,name,where,columns):
        columns=re.split(r'[, ]',str(columns))
        if(name=="FROM"):
            name=where
            dat=[]
            return name,dat,columns
        else:
            where=re.split(r'[= ]',str(where))
            dat=[]
            for i in range(2,len(where),3):
                col=where[i-1]
                col.replace("'","")
                data=where[i]
                data.replace("'","")
                if self.IsImageQuery(data):
                    route=self.TransformsRO(data)
                    img=image(route)
                    data=img      
                dat.append(col)
                dat.append(data)       
            return name,dat,columns
    def IsImageQuery(self,dat):
        if "Route("and")" in dat:
            return True
        else:
            return False
    def TransformsRO(self,route):
        start = route.find('(')
        end = route.find(')', start)
        route = route[start + 1:end]
        route=route.replace("'","")
        return route
                    
        
        
            
        
        
       
        