import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow import keras
import numpy as np
# from keras._tf_keras.keras.applications.resnet50 import ResNet50
# from keras._tf_keras import keras
from sklearn.model_selection import train_test_split
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import shutil
import os
import time

# subprocess.run(['python', 'mat_to_csv.py'])
# subprocess.run(['python', 'reduzir_csv.py'])
# if os.path.exists('atores'):
#   shutil.rmtree('atores')
# subprocess.run(['python', 'data_image_set.py'])

ids = pd.read_csv("ids.csv")

def actor(id:int):
  return str(ids[ids['id'] == id]['name'].iloc[0])

data_dir = "atores"
batch_size = 32
img_height = 244
img_width = 244

train_ds = keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=777,
  image_size=(img_height, img_width),
  batch_size=batch_size
)

val_ds = keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size
)

# plt.figure(figsize=(8, 8))
# for images, labels in train_ds.take(1):
#   for i in range(25):
#     ax = plt.subplot(5, 5, i + 1)
#     plt.imshow(images[i].numpy().astype("uint8"))
#     plt.title(actor(int(class_names[labels[i]])))
#     plt.axis("off")

# plt.show()

# from tensorflow.keras import mixed_precision
from keras._tf_keras.keras import mixed_precision
mixed_precision.set_global_policy('mixed_float16')

AUTOTUNE = tf.data.AUTOTUNE

class_names = train_ds.class_names

base_model = ResNet50(weights='imagenet', input_shape=(img_height, img_width, 3), include_top=False)
base_model.trainable = False

x = keras.layers.GlobalAveragePooling2D()(base_model.output)
x = keras.layers.Dense(128, activation='relu')(x)
x = keras.layers.Dense(len(class_names), activation='softmax')(x)

model = keras.Model(inputs=base_model.input, outputs=x)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

epochs = 5
ini = time.time()
with tf.device('/GPU:0'):
  history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs,
  )
fim = time.time()

model.save("meu_modelo.keras")

print(f"Tempo de execução: {fim - ini:.2f} segundos")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
