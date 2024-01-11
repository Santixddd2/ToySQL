
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
    def comparation(self,image):
        return 0
    def to_vector(self):
        image=self.image.reshape((1,28,28))
        vector=self.convolutional_model.predict(image)
        return vector