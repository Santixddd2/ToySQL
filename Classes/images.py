
import numpy as np
from PIL import Image
import tensorflow as tf
from Config.config import convolutional_model,clasification_model
class image:
    def __init__(self,route):
        self.route=route
        try:
           self.image= np.array(Image.open(self.route))
        except:
            print("Image not found")
        self.convolutional_model=tf.keras.models.load_model(convolutional_model)
        self.clasification_model=tf.keras.models.load_model(clasification_model)
    def summary(self):
        self.convolutional_model.summary()
        self.clasification_model.summary()
    def comparation(self,matrix):
        vector=self.to_vector()
        difference=matrix-vector
        difference=np.abs(difference)
        predictions=self.clasification_model.predict(difference)
        vectors=[]
        for i in range(predictions.shape[0]):
            if predictions[i]>0.5:
                vectors.append(np.array_str(matrix[i]))
        return vectors
    def to_vector(self):
        image=self.image.reshape((1,28,28))
        vector=self.convolutional_model.predict(image)
        return vector