#Controller for use on other aplications.
from Database import Database
from sqlparser import parser
from kernel_schemas import kernel_schemas
import Config.config as config

class DatabaseController():
    def __init__(self,name,credentials):
        self.name=name
        self.credentials=credentials
        self.db=None
    
    def open_conection(self):
        db=kernel_schemas(self.name)
        val=db.read_schema()
        if val==None:
           print("Error")
        else: 
           self.db=db
           print("Conection opened")
    def close_conection(self):
        self.db=None
        
    def create_database(self,name):
        db=Database()
        db.create(name)
    
    def query(self,query):
        p=parser(query,self.db)
        p.QUERY()   
    
    
    #For later
    
    def validation(self):
        return 0
    
    def config(self,name,value):
        try:
           config.name=value
        except:
            print("Error with the value or name")
    
name="Humans"
credentials=[]
obj=DatabaseController(name,credentials)

obj.open_conection()
query="SELECT * FROM Setchs"
obj.query(query)