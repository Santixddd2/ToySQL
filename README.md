"ToySQL" is a small Python-based Database Management System (DBMS) project. Its purpose is to integrate an Artificial Neural Network (ANN) model at the kernel level to handle queries involving images.

How to Use:

Start by installing the required dependencies in a virtual Python environment.

Next, run the "ToySQL" file.

You can either create a new database or use existing ones within the project. Note that these databases are intended for testing purposes.

To perform queries similar to other Database Management Systems (DBMS), follow these steps for image comparison:

a. Create: Begin by creating a table, ensuring that the attribute type is set to "IMAGE". Example: CREATE TABLE Clothes (Name VARCHAR(10), Picture IMAGE)

b. Insert: Subsequently, insert data by specifying the image's path, which should be within the "Images" folder. Example: INSERT INTO Clothes VALUES("Coat", ../Images/fashion_mnist_image_1786.jpg)

c. SELECT: For image-based data retrieval, use the keyword "Route". Currently, all images must be located in the "Images" folder. Example: SELECT * FROM Clothes WHERE Picture = Route('../Images/fashion_mnist_image_1791.jpg')