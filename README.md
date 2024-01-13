# ToySQL

"ToySQL" is a small Python-based Database Management System (DBMS) project. Its purpose is to integrate an Artificial Neural Network (ANN) model at the kernel level to handle queries involving images.

How to use?

*First, install the requirements in a virtual python environment
*Then, run the "ToySQL" file
*You can create a new database or use the ones that already exist in the project, it should be noted that there are for testing
*You can make a query like other DBMS, but to compare images you have to follow some steps:
        Create:First create a table and the attribute's type has to be "IMAGE":
              Example: CREATE TABLE Clothes (Name VARCHAR(10),Picture IMAGE)
        Insert: Then you can insert data writting the image's route that has to
        be on the folder "Images":
              Example: INSERT INTO Clothes VALUES("Coat",../Images/fashion_mnist_image_1786.jpg)
        SELECT: To select data with image comparation you have to use the word "Route".
        For now all images has to be on the folder "Images":
              Example: SELECT * FROM Clothes WHERE Picture=Route('../Images/fashion_mnist_image_1791.jpg')       
        
