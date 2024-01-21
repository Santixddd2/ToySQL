#Attributes Manager
from bintrees import FastRBTree
import uuid

class kernel_attributes:
    def __init__(self,name,attributes):
        self.name=name
        self.attributes=attributes
        self.attributesT=FastRBTree()
    def create_table(self):
        for i in range(len(self.attributes)):
            self.attributesT[self.attributes[i].name]=self.attributes[i]
    def insert_table(self,dat):
        id=str(uuid.uuid4())
        columns=0 
        for i in range(len(self.attributes)):
           obj=self.attributesT[self.attributes[i].name]   
           columns=obj.check_type(dat[i],columns)   
        if len(self.attributes)==columns:
            for i in range (len(self.attributes)):
                obj=self.attributesT[self.attributes[i].name]  
                obj.insert(dat[i],id)
        else:
            print("error with datatype")
           
    def select_table(self,dat,columns):
        id=self.selection(dat)
        query=[]
        all=False
        if columns[0]=="*":  
            columns=self.attributes   
            all=True     
        try:
            for j in range(len(id)):
               for i in range(len(columns)):
                     if all:
                       obj=self.attributesT[columns[i].name]
                       d=obj.select_uuid(id[j])
                     else:
                        obj=self.attributesT[columns[i]]
                        d=obj.select_uuid(id[j])
                     query.append(d)
        except:
            print("Data not found")
        return query,columns
    def delete_table(self,dat):
        id=self.selection(dat)
        columns=self.attributes
        try:
            for j in range(len(id)):
               for i in range(len(columns)):
                    obj=self.attributesT[columns[i].name]
                    obj.delete_name(id[j])
                    obj.delete_uuid(id[j])
        except:
            print("Data not found")
    def update_table(self,set,dat):
        id=self.selection(dat)
        try:
            for j in range(len(id)):
               for i in range(0,len(set),2):
                    obj=self.attributesT[set[i]]
                    obj.update_name(id[j],set[i+1])
                    obj.update_uuid(id[j],set[i+1])
        except:
            print("Data not found")

#Relational algebra operations
    def selection(self,dat):
        if len(dat)>0:
            obj=self.attributesT[dat[0]]
            id_f=self.select_type(obj,dat[1])
            for i in range (0,len(dat),2):
                obj=self.attributesT[dat[i]]
                id_s=self.select_type(obj,dat[i+1])
                intersection = list(set(id_f).intersection(id_s))
                if len(intersection)>0:
                    id_f=id_s
                else: 
                    intersection=[]
                    print("Data not found")
                    return intersection
                
                return intersection
        else:
            intersec=self.attributes[0].select_all()
            for i in range(len(self.attributes)):
                ids=self.attributes[i].select_all()
                intersec=list(set(intersec).intersection(ids))
            return intersec
#Restrictions
    def select_type(self,obj,dat):
        if obj.type=="IMAGE":
            id_f=obj.select_image(dat)
        else:
            id_f=obj.select_name(dat)
        return id_f
        
    
            