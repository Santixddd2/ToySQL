#Parse class
import sqlparse 
import os
from Attributes import attribute
from kernel_schemas import kernel_schemas
import re
from images import image
from Config.config import types

class parser:
    def __init__(self,query,db):
        self.db=db
        self.query=query
        self.parsed=sqlparse.parse(self.query)
#This function is used to classify the querys
    def QUERY(self):
        statement=self.parsed[0]
        if statement.get_type()=="CREATE":
            self.CREATE(statement,self.db)
        if statement.get_type()=="INSERT":
            self.INSERT(statement,self.db)
        if statement.get_type()=="SELECT":
            self.SELECT(statement,self.db)
        if statement.get_type()=="DELETE":
            self.DELETE(statement,self.db)
        if statement.get_type()=="UPDATE":
            self.UPDATE(statement,self.db)
#This function is to create, it has string transformations to use the writting query
    def CREATE(self,statement,db):
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        attributes=self.TransformsC(attributes)
        attributes=self.clear_attributes(attributes)
        atr=[]
        columns=0
        for i in range(1,len(attributes),2):
            lenght=self.haslenght(attributes[i])
            reference=self.hasreference(name,attributes[i-1],attributes[i],db)
            Attribute=attribute(attributes[i-1],attributes[i],lenght,reference)
            atr.append(Attribute)
            columns=self.is_type(attributes[i],columns)
        if columns==len(attributes)/2 and reference[0]!="RError":
            db.append_schema(atr,name)
        else:
            print("Error with datatypes")
        
#This insert is to create, it has string transformations to use the writting query
    def INSERT(self,statement,db):
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        try: 
           attributes=self.TransformsA(str(attributes))
           db.insert_data(name,attributes,db)
        except:
            print("Sintax error")
        
#This select is to create, it has string transformations to use the writting query
    def SELECT(self,statement,db):
        name=str(statement.tokens[6])
        columns=str(statement.tokens[2])
        where=str(statement.tokens[-1])
        name,dat,columns=self.TransformsCO(name,where,columns)
        db.select_data(name,dat,columns)
    def DELETE(self,statement,db):
        name=str(statement.tokens[-3])
        where=str(statement.tokens[-1])
        #name,dat,columns=self.TransformsCO(name,where,columns)
        name,dat,columns=self.TransformsCO(name,where,"")
        db.delete_data(name,dat,db)    
    def UPDATE(self,statement,db):
        columns=str(statement.tokens[6])
        name=str(statement.tokens[2])
        where=str(statement.tokens[-1])
        name,set,cols=self.TransformsCO(name,"WHERE "+columns,"")
        name,where,columns=self.TransformsCO(name,where,"")
        db.update_data(name,set,where)
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
    #Transforms for select,delete and update
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
#Transformations if the consult is for images
    def IsImageQuery(self,dat):
        if "Route("and")" in dat:
            return True
        else:
            return False
#Transformation to get the route
    def TransformsRO(self,route):
        start = route.find('(')
        end = route.find(')', start)
        route = route[start + 1:end]
        route=route.replace("'","")
        return route
#For reserved words and features
    def haslenght(self,type):
        lenght=0
        if "(" and ")" in type:
            start = type.find('(')
            end = type.find(')', start)
            lenght = type[start + 1:end]
        return lenght
    
    def hasreference(self,name,atr,type,db):
        type=type+"))"
        reference=[""]
        if "FOREIGNKEY" and "REFERENCE" in type:
            type=type+"))"
            type=type.split()
            type=type[2]
            schema=self.haslenght(type)
            schema=schema+")"
            attribute=self.haslenght(schema)
            schema=self.TransformsAtr(schema)
            try:
                db.save_reference(schema,attribute,name,atr)
                reference[0]=schema
                reference.append(attribute) 
                
            except:
                print("Reference error")
                reference.append("RError")
        return reference
            
    
    def TransformsAtr(self,type):
        if "("  in type:
            type = type.split("(")
            return type[0]
        else:
            return type
        
    def clear_attributes(self,attributes):
        try: 
            for j in range (len(attributes)):
                if self.TransformsAtr(attributes[j+1]) in types and self.TransformsAtr(attributes[j]) in types:
                    val=j+1
                    while self.TransformsAtr(attributes[val]) in types:
                        attributes[j]=attributes[j]+" "+attributes[val]
                        del attributes[val]
        except:
            pass
        return attributes
        
    def is_type(self,type,columns):
        #type=self.TransformsAtr(type)
        type=self.TransformsAtr(str(type))
        cont=0
        type=type.split()
        before=type[0]  
        for i in range (len(type)):                  
            if str(type[i]) in types:
                if i+1==len(type) and before in types:
                    cont=cont+1
        return columns+cont


                
            


                    
        
        
            
        
        
       
        