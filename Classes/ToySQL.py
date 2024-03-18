import sqlparse 
import os
import re
from .config import *
from bintrees import FastRBTree
import pickle
import uuid
import numpy as np
from PIL import Image
import tensorflow as tf

#Controller

'''
Esta clase funciona para interactuar con una base de datos. Proporciona métodos para abrir y cerrar conexiones, crear bases de datos ejecutar consultas y (potencialmente) manejar configuraciones.
'''
class DatabaseController():
    def __init__(self): #Constructor
        self.db=None
    
    def open_conection(self,route,credentials): #Este método se encarga de establecer una conexión a la base de datos.
        directorio_actual = os.getcwd()
        print("Directorio Actual:", directorio_actual)
        db=kernel_schemas(route)
        print(db)
        val=db.read_schema()
        if val==None:
           print("Error")
        else: 
           self.db=db
           print("Conection open")

    def close_conection(self): #Este método se encarga de cerrar la conexión a la base de datos.
        self.db=None
        
    def create_database(self,name,route): #Este método está diseñado para crear una nueva base de datos.
        db=Database()
        db.create(name,route)
    
    def query(self,query): #Este método ejecuta una consulta SQL en la base de datos.
        p=parser(query,self.db)
        data=p.QUERY()   
        return data
        
    #For later
    
    def validation(self):
        return 0

    def config(self,name,value):
        #try:
           #config.name=value
        #except:
            #print("Error with the value or name")
        return 0


#Daatabase manager

'''
Esta clase sirve para gestionar la creación de archivos de bases de datos
'''
class Database:
    def __init__(self): #Constructor
        self.databases=[]

    def append(self,database): #Agrega un nuevo nombre de base de datos a la lista self.databases. 
        self.databases.append(database)

    def create(self,name,route): #Crea un nuevo archivo de base de datos con la extensión .dat.
        file=route+name+".dat"
        with open(file, "w") as file:
            pass
        print("Database ",name," created succsefully")
        

#Sqlparser

'''
Esta clase se encarga del análisis y ejecución de consultas SQL dentro del sistema de base de datos. Toma una cadena de consulta y una referencia al objeto Database como entrada, analiza el tipo de consulta (CREAR, INSERTAR, SELECCIONAR, ELIMINAR, ACTUALIZAR) y delega la ejecución a los métodos correspondientes.
''' 
class parser:
    def __init__(self,query,db): #Constructor
        self.db=db
        self.query=query
        self.parsed=sqlparse.parse(self.query)

    def QUERY(self): #Este es el método principal que maneja el análisis y la ejecución de la consulta.
        statement=self.parsed[0]
        if statement.get_type()=="CREATE":
            self.CREATE(statement,self.db)
        if statement.get_type()=="INSERT":
            self.INSERT(statement,self.db)
        if statement.get_type()=="SELECT":
            data=self.SELECT(statement,self.db)
            return data
        if statement.get_type()=="DELETE":
            self.DELETE(statement,self.db)
        if statement.get_type()=="UPDATE":
            self.UPDATE(statement,self.db)

    #This function is to create, it has string transformations to use the writting query
    def CREATE(self,statement,db): #Maneja la creación de un nuevo esquema de base de datos.
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        attributes=self.TransformsC(attributes)
        attributes=self.clear_attributes(attributes)
        atr=[]
        columns=0
        for i in range(1,len(attributes),2):
            lenght=self.haslenght(attributes[i])
            reference=self.hasreference(name,attributes[i-1],attributes[i],db)
            Attribute=attribute(attributes[i-1],attributes[i],lenght,reference)
            atr.append(Attribute)
            columns=self.is_type(attributes[i],columns)
        if columns==len(attributes)/2 and reference[0]!="RError":
            db.append_schema(atr,name)
        else:
            print("Error with datatypes")
        
    #This insert is to create, it has string transformations to use the writting query
    def INSERT(self,statement,db): #Se encarga de insertar datos en una base de datos existente.
        name=str(statement.tokens[-3])
        attributes=statement.tokens[-1]
        try: 
           attributes=self.TransformsA(str(attributes))
           db.insert_data(name,attributes,db)
        except:
            print("Sintax error")
        
    #This select is to create, it has string transformations to use the writting query
    def SELECT(self,statement,db): #Maneja la selección de datos de una base de datos.
        #Extrae el nombre de la base de datos, las columnas objetivo y la cláusula WHERE opcional de la sentencia analizada.
        name=str(statement.tokens[6])
        columns=str(statement.tokens[2])
        where=str(statement.tokens[-1])
        name,dat,columns=self.TransformsCO(name,where,columns)
        data=db.select_data(name,dat,columns)
        #print(data)
        return data
        
    def DELETE(self,statement,db): #Maneja la eliminación de datos de una base de datos.
        name=str(statement.tokens[-3])
        where=str(statement.tokens[-1])
        #name,dat,columns=self.TransformsCO(name,where,columns)
        name,dat,columns=self.TransformsCO(name,where,"")
        db.delete_data(name,dat,db)

    def UPDATE(self,statement,db): #Maneja la actualización de datos en una base de datos
        columns=str(statement.tokens[6])
        name=str(statement.tokens[2])
        where=str(statement.tokens[-1])
        name,set,cols=self.TransformsCO(name,"WHERE "+columns,"")
        name,where,columns=self.TransformsCO(name,where,"")
        db.update_data(name,set,where)

    
    #STRING TRANSFORMATIONS

    #Transforms for create
    def TransformsC(self,attributes):
        attributes=re.split(r'[, ]',str(attributes))
        attributes[0]=attributes[0].replace("(","")
        attributes[len(attributes)-1]=attributes[len(attributes)-1].replace(")","")
        return attributes

    #Transforms for Insert
    def TransformsA(self,attributes):
        attributes=re.split(r'[, (]',str(attributes))
        del attributes[0]
        attributes[len(attributes)-1]=re.split(r'[, ]',attributes[len(attributes)-1])
        attributes[0]=str(attributes[0]).replace("(","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace(")","")
        attributes[0]=str(attributes[0]).replace("'","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("'","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("[","")
        attributes[len(attributes)-1]=str(attributes[len(attributes)-1]).replace("]","")
        return attributes

    #Transforms for select,delete and update
    def TransformsCO(self,name,where,columns):
        columns=re.split(r'[, ]',str(columns))
        if(name=="FROM"):
            name=where
            dat=[]
            return name,dat,columns
        else:
            where=re.split(r'[= ]',str(where))
            dat=[]
            for i in range(2,len(where),3):
                col=where[i-1]
                col.replace("'","")
                data=where[i]
                data.replace("'","")
                if self.IsImageQuery(data):
                    route=self.TransformsRO(data)
                    img=image(route)
                    data=img      
                dat.append(col)
                dat.append(data)   
            return name,dat,columns

    #Transformations if the consult is for images
    def IsImageQuery(self,dat):
        if "Route("and")" in dat:
            return True
        else:
            return False

    #Transformation to get the route
    def TransformsRO(self,route):
        start = route.find('(')
        end = route.find(')', start)
        route = route[start + 1:end]
        route=route.replace("'","")
        return route

    #For reserved words and features
    def haslenght(self,type):
        lenght=0
        if "(" and ")" in type:
            start = type.find('(')
            end = type.find(')', start)
            lenght = type[start + 1:end]
        return lenght
    
    def hasreference(self,name,atr,type,db):
        type=type+"))"
        reference=[""]
        if "FOREIGNKEY" and "REFERENCE" in type:
            type=type+"))"
            type=type.split()
            type=type[2]
            schema=self.haslenght(type)
            schema=schema+")"
            attribute=self.haslenght(schema)
            schema=self.TransformsAtr(schema)
            try:
                db.save_reference(schema,attribute,name,atr)
                reference[0]=schema
                reference.append(attribute) 
                
            except:
                print("Reference error")
                reference.append("RError")
        return reference
    
    def TransformsAtr(self,type):
        if "("  in type:
            type = type.split("(")
            return type[0]
        else:
            return type
        
    def clear_attributes(self,attributes):
        try: 
            for j in range (len(attributes)):
                if self.TransformsAtr(attributes[j+1]) in types and self.TransformsAtr(attributes[j]) in types:
                    val=j+1
                    while self.TransformsAtr(attributes[val]) in types:
                        attributes[j]=attributes[j]+" "+attributes[val]
                        del attributes[val]
        except:
            pass
        return attributes
        
    def is_type(self,type,columns):
        #type=self.TransformsAtr(type)
        type=self.TransformsAtr(str(type))
        cont=0
        type=type.split()
        before=type[0]  
        for i in range (len(type)):                  
            if str(type[i]) in types:
                if i+1==len(type) and before in types:
                    cont=cont+1
        return columns+cont


#Kernel schemas 

'''
Esta clase sirve para administrar esquemas (estructuras de bases de datos) dentro del sistema. Se encarga de crear, leer, insertar, seleccionar, eliminar y actualizar datos dentro de estos esquemas. También gestiona referencias entre esquemas y mantiene el archivo general de la base de datos
'''
class kernel_schemas:
    def __init__(self,db_name): #Constructor
        self.db_name=db_name
        self.schemas=FastRBTree()

    def append_schema(self,attributes,name): #Crea un nuevo objeto de esquema (kernel_attributes) con el nombre proporcionado (name) y las definiciones de atributos (attributes).

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

    def read_schema(self): #Se encarga de leer los esquemas existentes del archivo de la base de datos
        #try:
            with open(self.db_name,"rb") as fil:
                while True:
                    try:
                        print("archivo ",fil)
                        obj=pickle.load(fil)
                        name=obj.name
                        self.schemas[name]=obj
                        print("Schema ",name," charged succsefully")
                    except EOFError:
                      break
            return 0
        #except Exception as e:
            #print("Database ",self.db_name," doesn't exist")
            #return None

    def insert_data(self,schema,data,db): #Se encarga de recuperar el objeto de esquema con el nombre dado (schema) del almacenamiento interno (self.schemas). INSERT
        try:
            ka=self.schemas[schema]
            ka.insert_table(data,db)
            self.save_file()
        except: 
            print("Schema doesn't founded")
            
    def select_data(self,name,dat,columns): #Intenta recuperar el objeto de esquema con el nombre dado (name) del almacenamiento interno (self.schemas). SELECT
        try:
            ka=self.schemas[name]
            r,columns=ka.select_table(dat,columns)
            data=self.return_data(columns,r)
            #print(data)
            return data
        except:
            print("Data not found")    
            return 0  

    def delete_data(self,name,dat,db): #Eliminación de datos
        try:
            ka=self.schemas[name]
            ka.delete_table(dat,db)
            self.save_file()
            #print("Data deleted succesfully")
        except:
            print("Data not found")

    def update_data(self,name,set,dat): #Actualización de datos
        try:
            ka=self.schemas[name]
            ka.update_table(set,dat)
            self.save_file()
            print("Data updated succesfully")
        except:
            print("Data not found")    

    def print_data(self,columns,r): #Presentación de datos
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
    
    def save_reference(self,schema,attribute,name,atr): #Administra referencias entre esquemas
        self.schemas[schema].reference_table(attribute,name,atr)
        self.save_file()
         
    def get_schema(self,name): #Comprueba si existe un esquema con el nombre dado (name).
        try:
           x=self.schemas[name]
           return False
        except:
            return True

    def save_file(self): #Guarda los esquemas en un archivo
        temp,ext= os.path.splitext(self.db_name)
        temp=temp+"_temp"+ext
        values = list(self.schemas.values())
        for value in values:
            schema=value
            with open(temp,"ab") as fil:
                pickle.dump(schema, fil)
        os.remove(self.db_name)
        os.rename(temp,self.db_name)
    
    def return_data(self,columns,r): #Formatea y organiza los datos para su presentación y devuelve el diccionario con los datos formateados
        dic={}
        for i in range(0,len(r),len(columns)):
            dat=[]
            R=i+len(columns)
            for j in range(i,R,1):
                try:
                    dic[str(columns[j-i].name)].append(r[j].data)
                except:
                    dat=[]
                    dic[str(columns[j-i].name)]=dat
                    dic[str(columns[j-i].name)].append(r[j].data)
                    
        return dic
    

#kernel attributes

'''
La clase kernel_attributes representa un esquema individual dentro de la base de datos. Se encarga de administrar los atributos (columnas) del esquema y proporciona métodos para crear, manipular y consultar los datos asociados.
'''
class kernel_attributes:
    def __init__(self,name,attributes): #Constructor
        self.name=name
        self.attributes=attributes
        self.attributesT=FastRBTree()

    #Construye el árbol attributesT iterando sobre la lista de atributos (attributes).Por cada atributo, lo agrega al árbol usando su nombre como clave.
    def create_table(self):
        for i in range(len(self.attributes)):
            self.attributesT[self.attributes[i].name]=self.attributes[i]

    def insert_table(self,dat,db): #Inserta nuevos datos en el esquema
        id=str(uuid.uuid4())
        id=None
        columns=0 
        for i in range(len(self.attributes)):
           obj=self.attributesT[self.attributes[i].name]   
           if obj.is_primary() and id==None:
               id=dat[i]            
           columns=obj.check_type(dat[i],columns)   
        if id==None:
            id=str(uuid.uuid4())   
        if len(self.attributes)==columns:
            for i in range (len(self.attributes)):
                obj=self.attributesT[self.attributes[i].name]  
                obj.insert(dat[i],id,db)
        else:
            print("error with datatype")
           
    #Selecciona datos del esquema el cual llama al método selection(dat) para obtener los identificadores (id) coincidentes con las condiciones de selección (lógica WHERE).
    def select_table(self,dat,columns):
        id=self.selection(dat)
        query=[]
        all=False
        if columns[0]=="*":  
            columns=self.attributes   
            all=True     
        try:
            for j in range(len(id)):
               for i in range(len(columns)):
                     if all:
                       obj=self.attributesT[columns[i].name]
                       d=obj.select_uuid(id[j])
                     else:
                        obj=self.attributesT[columns[i]]
                        d=obj.select_uuid(id[j])
                     query.append(d)
        except:
            print("Data not found")
        return query,columns
    
    #Elimina datos del esquema el cual llama al método selection(dat) para obtener los identificadores (id) coincidentes con las condiciones de selección (lógica WHERE).
    def delete_table(self,dat,db):
        id=self.selection(dat)
        columns=self.attributes
        try:
            for j in range(len(id)):
                if self.reference_comprobation(columns,db,id[j],"Delete")==len(columns):
                    for i in range(len(columns)):
                        obj=self.attributesT[columns[i].name]
                        obj.delete_name(id[j])
                else:
                    print("Rerror")    
        except:
            print("Data not found")
    
    #Actualiza datos del esquema el cual llama al método selection(dat) para obtener los identificadores (id) coincidentes con las condiciones de selección (probable lógica WHERE).
    def update_table(self,set,dat):
        id=self.selection(dat)
        try:
            for j in range(len(id)):
               for i in range(0,len(set),2):
                    obj=self.attributesT[set[i]]
                    obj.update_name(id[j],set[i+1])
                    obj.update_uuid(id[j],set[i+1])
        except:
            print("Data not found")

    #Establece una referencia entre atributos el cual se encarga de acceder al objeto de atributo especificado por attribute dentro del árbol attributesT.
    def reference_table(self,attribute,name,atr):
        try:
           self.attributesT[attribute].referenced[name]=atr
        except:
            print("Attribute error")

    #Relational algebra operations
    #Realiza la selección de datos basado en condiciones (lógica WHERE) Si la lista de selección (dat) está vacía, significa que se quieren todos los datos.
    def selection(self,dat):
        if len(dat)>0:
            obj=self.attributesT[dat[0]]
            id_f=self.select_type(obj,dat[1])
            for i in range (0,len(dat),2):
                obj=self.attributesT[dat[i]]
                id_s=self.select_type(obj,dat[i+1])
                intersection = list(set(id_f).intersection(id_s))
                if len(intersection)>0:
                    id_f=id_s
                else: 
                    intersection=[]
                    print("Data not found")
                    return intersection
                
                return intersection
        else:
            intersec=self.attributes[0].select_all()
            for i in range(len(self.attributes)):
                ids=self.attributes[i].select_all()
                intersec=list(set(intersec).intersection(ids))
            return intersec

    #Restrictions
    #Delega la selección basada en el tipo de atributo si es imagen o no
    def select_type(self,obj,dat):
        if obj.type=="IMAGE":
            id_f=obj.select_image(dat)
        else:
            id_f=obj.select_name(dat)
        return id_f

    #Comprobations
    #Verifica referencias a otros esquemas antes de realizar eliminaciones
    def reference_comprobation(self,columns,db,dat,type):
       cont=0
       for i in range(len(columns)):
            obj=self.attributesT[columns[i].name]
            cont=obj.reference_comprobation(dat,db,cont,type)
       return cont
   

#Attributes

'''
La clase attribute representa un atributo (columna) individual dentro de un esquema (tabla) de la base de datos. Se encarga de almacenar y administrar los datos asociados al atributo, además de realizar validaciones y comprobaciones referenciales.
'''
class attribute:
    #Initialization of parameters, if is image, the object has a feautre matrix and a FastRBTree of uuid's, 
    # if it isn't has two FastRBTrees
    def __init__(self,name,type,lenght,reference):
        self.name=name
        self.type=type
        self.lenght=int(lenght)
        self.reference=reference
        self.referenced={}
        if self.type=="IMAGE":
            self.reference_matrix=np.empty((1,vector_size))
            self.image_vector=np.empty((height,weight))
        self.data=FastRBTree()
        self.uuid=FastRBTree()

    #Two methos to insert images or normal data
    def insert(self,dat,id,db): #Inserta nuevos datos en el atributo.
        if id in self.uuid or self.reference_integrity(db,dat,"Insert")==False:
            print("Error with primary key or reference integrity")
        else:
            if self.type=="IMAGE":
               self.insert_image(dat,id)
            else:
               self.insert_normal(dat,id)  

    #Function to insert images         
    def insert_image(self,dat,id):
        try:
           d=data(dat,id)  
           self.uuid[id]=d
           img=image(dat)
           img=img.to_vector()
           key=''.join(map(str, list(img)))
           if key in self.data:
               self.data[key].append(id)
               self.uuid[d.id]=d
               print("Insert saved")
           else:
               dataH=[]
               dataH.append(id)
               self.data[key]=dataH
               self.reference_matrix=np.vstack((self.reference_matrix, img))
               print("Insert saved")
        except:
            print("Something wrong with the image")

    #Function to insert normal data
    def insert_normal(self,dat,id):
        try:
           d=data(dat,id)           
           if d.data in self.data:
               self.data[d.data].append(d.id)
               self.uuid[d.id]=d
               print("Insert saved")
           else:
               dataH=[]
               dataH.append(d.id)
               self.data[d.data]=dataH
               self.uuid[d.id]=d
               print("Insert saved")
        except:
            print("Something wrong with insert query, please review and try again")

    #These functions are responsible for the selection
    def select_name(self,dat): #Recupera todos los identificadores asociados al valor (dat) del atributo en el árbol data.
        return self.data[dat]

    def select_uuid(self,dat): #Recupera el objeto data asociado al identificador (dat) del atributo en el árbol uuid.
        return self.uuid[dat]

    def select_all(self): #Obtiene una lista con todos los identificadores únicos (uuid) almacenados en el atributo.
        all_ids = []
        for key, value in self.data.items():
            all_ids.extend(value)
        return all_ids

    def select_image(self,img): #Recupera los identificadores asociados a imágenes similares a la imagen proporcionada (img).
        ids=[]
        vectors=img.comparation(self.reference_matrix)
        for i in range(len(vectors)):
            for j in range(len(self.data[vectors[i]])):
                ids.append(self.data[vectors[i]][j])
        return ids

    def delete_uuid(self,dat): #Elimina el objeto data asociado al identificador (dat) del árbol uuid.
        del self.uuid[dat]

    def delete_name(self,dat): #Elimina los datos asociados al valor (dat) del atributo.
        dat=self.select_uuid(dat)
        if dat.data in self.data:
            del self.data[dat.data]
            self.delete_uuid(dat.id)
        else:
            pass
            
    def update_name(self,dat,set): #Actualiza el valor del atributo asociado a un identificador.
        dat=self.select_uuid(dat)
        if dat.data in self.data:
           dataH=self.data[dat.data]
           del self.data[dat.data]
           self.data[set]=dataH
        else:
            pass

    def update_uuid(self,dat,set): #Actualiza el valor del dato (set) en el objeto data asociado al identificador (dat) del árbol uuid.
        self.uuid[dat].data=set

    #Type validation
    #Verifica si el tipo de dato (data) es compatible con el tipo de atributo
    def check_type(self,data,columns):
        if "VARCHAR" in self.type.upper():
            if len(data)<self.lenght:
                return columns+1
            else:
                return 0
        if  eval(self.type.lower())==int:
            try: 
                data=int(data)
                return columns+1
            except:
                print("Invalid data")
                return 0
        if  eval(self.type.lower())==float:
            try: 
                data=float(data)
                return columns+1
            except:
                print("Invalid data")
                return 0
        if "IMAGE" in self.type.upper():
            img=image(data)
            if isinstance(img.image, np.ndarray):
                return columns+1
            else:
                return 0
        if "PRIMARYKEY" in self.type.upper():
            pass
        else:
            print("Invalid data")
            return 0

    def is_primary(self): #Indica si el atributo es una clave primaria (PRIMARYKEY).
        if "PRIMARYKEY" in self.type.upper():
            return True
        else:
            return False

    #For reference
    #Comprueba la integridad referencial antes de realizar inserciones, actualizaciones o eliminaciones:
    def reference_integrity(self,db,dat,type):
        if len(self.reference)>1:
            try:
                x=db.schemas[self.reference[0]].attributesT[self.reference[1]].data[dat]
                return True
            except:
                return False
            
        elif len(self.referenced)>0 and type=="Delete" or type=="Update":
            print("Passss")
            for key in self.referenced:
                dat=self.select_uuid(dat)
                dat=dat.data
                try:
                   db.schemas[key].attributesT[self.referenced.get(key)].data[dat]
                   return False
                except:
                    pass
            return True
        else:
            return True

    #No está claro su propósito exacto, pero aparentemente realiza comprobaciones referenciales adicionales y gestiona contadores.
    def reference_comprobation(self,dat,db,i,type):
        if self.reference_integrity(db,dat,type):
            print("hey self")
            return i+1
        else:
            print(":(")
            return i+0


#Data 

'''
Esta clase se encarga de almacenar y recuperar el valor del dato y su identificador.
'''
class data:
    def __init__(self,data,id):
        self.data=data
        self.id=id


#Images

'''
Representa imágenes y realiza operaciones de comparación con otras imágenes utilizando modelos de aprendizaje profundo.
'''
class image:
    def __init__(self,route): #Constructor
        self.route=route
        try:
           self.image= np.array(Image.open(self.route))
        except:
            self.image=0
            print("Image not found")
        self.convolutional_model=tf.keras.models.load_model(convolutional_model)
        self.clasification_model=tf.keras.models.load_model(clasification_model)
    
    #Imprime un resumen de la arquitectura de los modelos convolucional y de clasificación.
    def summary(self):
        self.convolutional_model.summary()
        self.clasification_model.summary()
        
    #Compara la imagen actual con una matriz de vectores de características, obtiene el vector de características de la imagen actual usando el modelo convolucional y alcula la diferencia absoluta entre el vector de características y cada vector en la matriz. Utiliza el modelo de clasificación para predecir la similitud entre la imagen actual y cada vector de la matriz y evuelve los vectores de la matriz cuya predicción de similitud supera un umbral determinado (umbral).
    def comparation(self,matrix):
        vector=self.to_vector()
        difference=matrix-vector
        difference=np.abs(difference)
        predictions=self.clasification_model.predict(difference)
        vectors=[]
        for i in range(predictions.shape[0]):
            if predictions[i]>umbral:
                vectors.append(np.array_str(matrix[i]))
        return vectors
    
    #Convierte la imagen actual a un vector de características usando el modelo convolucional,  redimensiona la imagen a la forma requerida por el modelo convolucional y evuelve el vector de características obtenido.
    def to_vector(self):
        image=self.image.reshape((1,height,weight))
        vector=self.convolutional_model.predict(image)
        return vector