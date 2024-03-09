from Classes.controller import DatabaseController
import os
name="DataBases\Pruebas.dat"
credentials=[]
obj=DatabaseController()
obj.open_conection(name,credentials)