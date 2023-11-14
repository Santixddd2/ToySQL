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
        for i in range(len(self.attributes)):
           obj=self.attributesT[self.attributes[i].name]      
           obj.insert(dat[i],id)
            