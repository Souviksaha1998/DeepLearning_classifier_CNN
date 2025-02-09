# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HJAPeqNj4k9HiqQWzpp6P7iuRo5uEnYX
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from PIL import Image

!unzip cats.zip

pip install pillow

!unzip dogs.zip

import os
import cv2

x = [] #categories
y = []  #number
cat_folder = 'cats'
dogs_folder = 'dogs'
name_decode = {"cats": 0 , "dogs":1}
def img_to_array(folder  , name):
  for image in os.listdir(folder):
    image1 = Image.open(os.path.join(folder,image))
    resize_img = Image.Image.resize(image1 ,[100,100])
    array_img = np.array(resize_img)
    x.append(array_img)
    y.append(name_decode[name])

    flip = cv2.flip(array_img , 1)
    x.append(flip)
    y.append(name_decode[name])

    blur = cv2.blur(array_img,(2,2))
    x.append(blur)
    y.append(name_decode[name])
  
def show_img(index):
  plt.imshow(x[index])
  plt.show()
  print(y[index])

img_to_array(cat_folder , 'cats')
img_to_array(dogs_folder , 'dogs')
y = to_categorical(y , num_classes=2)
x = (np.array(x) - 127.5)/127.5

show_img(68)

from keras.models import Sequential
from keras.layers import Dense , Conv2D , MaxPool2D , Flatten , Dropout , Activation , BatchNormalization

model = Sequential()
model.add(Conv2D(32 , (5,5), padding='same' ,input_shape=(100,100,3)))
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Conv2D(100 , (3,3), padding='same' ,input_shape=(100,100,3)))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Conv2D(100 , (3,3), padding='same' ,input_shape=(100,100,3)))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(124))
model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('sigmoid'))

from keras.optimizers import Adam

optimizer = Adam(learning_rate=0.001)
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10)

print(y[40])
show_img(40)

model.compile(optimizer=optimizer  , loss ='binary_crossentropy' , metrics=['accuracy'])
model.fit(x_train , y_train , batch_size=10 , epochs=2000 , validation_data=(x_test , y_test))

model.save('cnn_dog.h5')

plt.plot(model.history.history['accuracy'])
plt.plot(model.history.history['val_accuracy'])

model.predict_classes(x_test)

# def prediction(index):
#   array = (np.array(x[index])-127.5)/127.5
#   array = array.reshape(1,100,100,3)
#   prediction = model.predict_classes(array)
#   print(prediction[0])
#   plt.imshow(x[index])
#   plt.show()

from keras.models import load_model
model = load_model('cnn_dog.h5')

img = Image.open('s.jpg')
plt.imshow(img)
img1 =Image.Image.resize(img,[100,100])
img2 = (np.array(img1)-127.5)/127.5
img3 = img2.reshape(1,100,100,3)
predict = model.predict_classes(img3)
if predict == 0:
  print('Its a cat')
  plt.imshow(img1)
else:
  print('Its a dog')
  plt.imshow(img1)

