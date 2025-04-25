# import tensorflow as tf
# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from keras._tf_keras.keras.applications.resnet50 import ResNet50
from keras._tf_keras.keras.preprocessing import image
from keras._tf_keras.keras.applications.resnet50 import preprocess_input, decode_predictions
from tkinter import Tk
from tkinter.filedialog import askdirectory

# ResNet50
model = ResNet50(weights='imagenet')

Tk().withdraw() # nao abrir a janela do tk
dataset_folder = askdirectory()

# Load and preprocess the image
img_path = 'nm0001303_rm1733604864_1971-8-29_2011.jpg'
img = image.load_img(img_path)
x = image.img_to_array(img)

# Use the model to classify the image
preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])