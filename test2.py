
from Classes.ToySQL import *
from Classes.config import *
name="DataBases\Pruebas2.dat"
credentials=[]
obj=DatabaseController()
obj.open_conection(name,[])
query='SELECT * FROM Perros'
data=obj.query(query)
print(data)