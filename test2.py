from Classes.ToySQL import *
from Classes.config import *
name="DataBases\Prueba1.dat"
credentials=[]
obj=DatabaseController()
obj.open_conection(name,[])

# NAME BD
# query = 'CREATE TABLE client (nameC VARCHAR(20),idC INT)'
# query = 'CREATE TABLE product (nameP VARCHAR(20),idP INT)'

# INSERT BD CLIENT
# query = 'INSERT INTO client VALUES("Mayer",1)'
# query = 'INSERT INTO client VALUES("Sebas",2)'
# query = 'INSERT INTO client VALUES("Santi",3)'

# INSERT BD PRODUCT
# query = 'INSERT INTO product VALUES("Potato",1)'
# query = 'INSERT INTO product VALUES("Carrot",2)'
# query = 'INSERT INTO product VALUES("Bear",3)'

# SELECT CLIENT
# query='SELECT * FROM client'

# SELECT PRODUCT
# query='SELECT * FROM product'

# SELECT JOIN CLIENT - PRODUCT
# query='SELECT * FROM product INNER JOIN client ON product.idP = client.idC'
query='SELECT nameP,nameC FROM product INNER JOIN client ON product.idP = client.idC'

data=obj.query(query)
print(data)