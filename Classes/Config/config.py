#This is config document,currently you can configurate some variables about AI model and image size 

#If the model is in two blocks

convolutional_model="../Model/FirstB"
clasification_model="../Model/SecondB"

#Image shape 

height=28
weight=28

#Vector size 

vector_size=10

#Comparation Umbral

umbral=0.5

#If the model is in unique block(this function isn't programmed yet XD)

model=""

#Types of data

types=["INT","IMAGE","FLOAT","VARCHAR"]

#Credentials to use the database(this function is also not programmed yet XDD)

password=""
port=""
host=""