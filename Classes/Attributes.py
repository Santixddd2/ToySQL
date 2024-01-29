#Attributes Class
from bintrees import FastRBTree
from data import data
from images import image
import numpy as np
from Config.config import vector_size,height,weight

class attribute:
    #Initialization of parameters, if is image, the object has a feautre matrix and a FastRBTree of uuid's, 
    # if it isn't has two FastRBTrees
    def __init__(self,name,type,lenght):
        self.name=name
        self.type=type
        self.lenght=int(lenght)
        if self.type=="IMAGE":
            self.reference_matrix=np.empty((1,vector_size))
            self.image_vector=np.empty((height,weight))
        self.data=FastRBTree()
        self.uuid=FastRBTree()
    #Two methos to insert images or normal data
    def insert(self,dat,id):
        if id in self.uuid:
            print("Error with primary key")
        else:
            if self.type=="IMAGE":
               self.insert_image(dat,id)
            else:
               self.insert_normal(dat,id)  
    #Function to insert images         
    def insert_image(self,dat,id):
        try:
           d=data(dat,id)  
           self.uuid[id]=d
           img=image(dat)
           img=img.to_vector()
           key=''.join(map(str, list(img)))
           if key in self.data:
               self.data[key].append(id)
               self.uuid[d.id]=d
               print("Insert saved")
           else:
               dataH=[]
               dataH.append(id)
               self.data[key]=dataH
               self.reference_matrix=np.vstack((self.reference_matrix, img))
               print("Insert saved")
        except:
            print("Something wrong with the image")
    #Function to insert normal data
    def insert_normal(self,dat,id):
        try:
           d=data(dat,id)           
           if d.data in self.data:
               self.data[d.data].append(d.id)
               self.uuid[d.id]=d
               print("Insert saved")
           else:
               dataH=[]
               dataH.append(d.id)
               self.data[d.data]=dataH
               self.uuid[d.id]=d
               print("Insert saved")
        except:
            print("Something wrong with insert query, please review and try again")
    #These functions are responsible for the selection
    def select_name(self,dat):
        return self.data[dat]
    def select_uuid(self,dat):
        return self.uuid[dat]
    def select_all(self):
        all_ids = []
        for key, value in self.data.items():
            all_ids.extend(value)
        return all_ids
    def select_image(self,img):
        ids=[]
        vectors=img.comparation(self.reference_matrix)
        for i in range(len(vectors)):
            for j in range(len(self.data[vectors[i]])):
                ids.append(self.data[vectors[i]][j])
        return ids
    def delete_uuid(self,dat):
        del self.uuid[dat]
    def delete_name(self,dat):
        dat=self.select_uuid(dat)
        if dat.data in self.data:
           del self.data[dat.data]
        else:
            pass
    def update_name(self,dat,set):
        dat=self.select_uuid(dat)
        if dat.data in self.data:
           dataH=self.data[dat.data]
           del self.data[dat.data]
           self.data[set]=dataH
        else:
            pass
    def update_uuid(self,dat,set):
        self.uuid[dat].data=set
    #Type validation
    def check_type(self,data,columns):
        if "VARCHAR" in self.type.upper():
            if len(data)<self.lenght:
                return columns+1
            else:
                return 0
        if  eval(self.type.lower())==int:
            try: 
                data=int(data)
                return columns+1
            except:
                print("Invalid data")
                return 0
        if  eval(self.type.lower())==float:
            try: 
                data=float(data)
                return columns+1
            except:
                print("Invalid data")
                return 0
        if "IMAGE" in self.type.upper():
            img=image(data)
            if isinstance(img.image, np.ndarray):
                return columns+1
            else:
                return 0
        if "PRIMARYKEY" in self.type.upper():
            pass
        else:
            print("Invalid data")
            return 0
    def is_primary(self):
        if "PRIMARYKEY" in self.type.upper():
            return True
        else:
            return False
            
            
        
        