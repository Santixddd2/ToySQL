#Daatabase manager

class Database:
    def __init__(self):
        self.databases=[]
    def append(self,database):
        self.databases.append(database)
    def create(self,name,route):
        file=route+name+".dat"
        with open(file, "w") as file:
            pass
        print("Database ",name," created succsefully")
    


