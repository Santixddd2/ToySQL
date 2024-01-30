#Schemas Manager
import os
from bintrees import FastRBTree
from kernel_attributes import kernel_attributes
import pickle

class kernel_schemas:
    def __init__(self,db_name):
        self.db_name="../DataBases/"+db_name+".dat"
        self.schemas=FastRBTree()
    def append_schema(self,attributes,name):
        schema=kernel_attributes(name,attributes)
        if self.get_schema(schema.name):
            schema.create_table()
            try:
                with open(self.db_name,"ab") as fil:
                    pickle.dump(schema, fil)
                print("Schema ",schema.name," created succesfully, please enter again to the database")
            except Exception as e:
                print("Error: File doesn't exist or it is corrupted")
        else:
            print("This schema already exist")

    def read_schema(self):
        try:
            with open(self.db_name,"rb") as fil:
                while True:
                    try:
                       obj=pickle.load(fil)
                       name=obj.name
                       self.schemas[name]=obj
                       print("Schema ",name," charged succsefully")
                    except EOFError:
                      break
            return 0
        except Exception as e:
            print("Database ",self.db_name," doesn't exist")
            return None
    def insert_data(self,schema,data,db): 
        try:
            ka=self.schemas[schema]
            ka.insert_table(data,db)
            self.save_file()
        except: 
            print("Schema doesn't founded")
            

    def select_data(self,name,dat,columns):
        try:
            ka=self.schemas[name]
            r,columns=ka.select_table(dat,columns)
            self.print_data(columns,r)
        except:
            print("Data not found")      
    def delete_data(self,name,dat):
        try:
            ka=self.schemas[name]
            ka.delete_table(dat)
            self.save_file()
            print("Data deleted succesfully")
        except:
            print("Data not found")      
    def update_data(self,name,set,dat):
        try:
            ka=self.schemas[name]
            ka.update_table(set,dat)
            self.save_file()
            print("Data updated succesfully")
        except:
            print("Data not found")     
    def print_data(self,columns,r):
        col=""
        lim=""
        dat=""
        for h in range(len(columns)):
            try:
                col=col+"| "+ columns[h]+" |"
                lim=lim+"---------"
            except:
                col=col+"| "+ columns[h].name+" |"
                lim=lim+"---------"
        print(col)
        for i in range(0,len(r),len(columns)):
            print(lim)
            R=i+len(columns)
            for j in range(i,R,1):
                dat=dat+"| "+r[j].data
            print(dat)
            dat=""
                
    def get_schema(self,name):
        try:
           x=self.schemas[name]
           return False
        except:
            return True
    def save_file(self):
        temp,ext= os.path.splitext(self.db_name)
        temp=temp+"_temp"+ext
        values = list(self.schemas.values())
        for value in values:
            schema=value
            with open(temp,"ab") as fil:
                pickle.dump(schema, fil)
        os.remove(self.db_name)
        os.rename(temp,self.db_name)
    
        
        
    