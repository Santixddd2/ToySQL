#Attributes Class
import os
import sqlparse
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
        self.data[d.data]=d
        self.uuid[id]=d
        
        