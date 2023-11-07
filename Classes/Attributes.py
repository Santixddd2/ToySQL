#Attributes Class
import os
import sqlparse
from bintrees import FastRBTree

class attribute:
    def __init__(self,name,type):
        self.name=name
        self.type=type
        self.data=FastRBTree()
        
        