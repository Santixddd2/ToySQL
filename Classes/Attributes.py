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
        if d.data in self.data:
            self.data[d.data].append(d.id)
        else:
            dataH=[]
            dataH.append(d.id)
            self.data[d.data]=dataH
        self.uuid[d.id]=d
    def select_name(self,dat):
        return self.data[dat]
    def select_uuid(self,dat):
        return self.uuid[dat]
        
        