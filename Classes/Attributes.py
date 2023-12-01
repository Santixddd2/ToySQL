#Attributes Class
from bintrees import FastRBTree
from data import data

class attribute:
    def __init__(self,name,type):
        self.name=name
        self.type=type
        self.data=FastRBTree()
        self.uuid=FastRBTree()
    def insert(self,dat,id):
        d=data(dat,id)
        if self.check_type(d.data):
            if d.data in self.data:
               self.data[d.data].append(d.id)
            else:
               dataH=[]
               dataH.append(d.id)
               self.data[d.data]=dataH
            self.uuid[d.id]=d
            print("It is the datatype")
    def select_name(self,dat):
        return self.data[dat]
    def select_uuid(self,dat):
        return self.uuid[dat]
    def select_all(self):
        all_ids = []
        for key, value in self.data.items():
            all_ids.extend(value)
        return all_ids
    def check_type(self,data):
        if "VARCHAR" in self.type.upper():
            self.type="str"
        if  eval(self.type.lower())==int:
            try: 
                data=int(data)
                return True
            except:
                print("Invalid data")
                return False
        elif  eval(self.type.lower())==float:
            try: 
                data=float(data)
                return True
            except:
                print("Invalid data")
                return False
        elif  isinstance(data,eval(self.type.lower())):
            return True
        else:
            print("Invalid data")
            return False
            
            
        
        