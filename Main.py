import tensorflow as tf
from tensorflow.keras import Sequential

from tensorflow.keras.layers import Flatten,Dense,BatchNormalization,Conv2D,MaxPool2D,Dropout

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image

print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib as plt

from sklearn.model_selection import train_test_split
from tqdm import tqdm


data = pd.read_csv("Movies-Poster_Dataset/train.csv")

data.head(10)

img_width = 350
img_height = 350

x = []

for i in tqdm(range(data.shape[0])):
  path='Movies-Poster_Dataset/Images/'+ data['Id'][i]+'.jpg'
  img = image.load_img(path,target_size=(img_width,img_height))
  img = image.img_to_array(img)
  img = img/255.0
  x.append(img)

x = np.array(x)

x.shape

import matplotlib.pyplot as plt

plt.imshow(x[1])

data["Genre"][1]

y= data.drop(['Id','Genre'], axis=1)
y= y.to_numpy()
y.shape

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0,test_size=0.15)

model = Sequential()
model.add(Conv2D(16,(3,3),activation='relu', input_shape = x_train[0].shape))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.2))

model.add(Conv2D(32,(3,3),activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.3))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.4))

model.add(Conv2D(128,(3,3),activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(25, activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

history = model.fit(x_train,y_train,epochs=5,validation_data=(x_test,y_test))

img=image.load_img('oussama.jpg',target_size=(img_width,img_height,3))
plt.imshow(img)
img = image.img_to_array(img)
img= img/155.0

img=img.reshape(1,img_width,img_height,3)

classes = data.columns[2:]
print(classes)
y_prob = model.predict(img)
top3 = np.argsort(y_prob[0][:4:-1])
print(y_prob)

for i in range(3):
  print(classes[top3[i]])

from google.colab import drive
drive.mount('/content/drive')