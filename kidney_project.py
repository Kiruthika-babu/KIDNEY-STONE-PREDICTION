# -*- coding: utf-8 -*-
"""Kidney project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lKjCqZCaJQg4zO2m5DAQyoiFoMUlMBnY

KIDNEY STONE PREdICTION

1. BASICS
"""

import pandas as pd
import numpy as np
from fastbook import *

!pip install -Uqq fastbook
import fastbook
fastbook.setup_book()

from fastai.vision.all import *
path = Path('/content/gdrive/MyDrive/kidney')

"""To count the images"""

path = Path('/content/gdrive/MyDrive/kidney')
for folder in path.glob('*'):
    print(f"{folder}: {len(list(folder.glob('*')))}")

"""Preprocessing"""

import os
import numpy as np
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

"""preprocessing

"""

from keras.preprocessing.image import ImageDataGenerator

# Define the ImageDataGenerator for preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255, 
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest')


img_height = 224
img_width = 224
# Load the images from directory and apply data augmentation
train_generator = train_datagen.flow_from_directory(
    '/content/gdrive/MyDrive/kidney',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary')

import os
print(os.listdir('/content/gdrive/MyDrive/kidney/Normal'))

"""SPLIT

"""

!pip install split-folders
import os
import splitfolders 
input_folder = "/content/gdrive/MyDrive/kidney"
output = "/content/gdrive/MyDrive/new kidney"  
splitfolders.ratio(input_folder, output, seed=1337, ratio=(.75, .25))

"""MODEL

INCEPTION V3
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
# Define the model architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

from keras.models import Model
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers import GlobalAveragePooling2D

from keras.applications.inception_v3 import InceptionV3

img_height = 224
img_width = 224
num_classes = 2



# Load the InceptionV3 model without the top layers
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))

# Add custom top layers for our dataset
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Combine the base model and the custom top layers
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model with Adam optimizer and categorical crossentropy loss
model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

train_dir = '/content/gdrive/MyDrive/new kidney/train'
num_classes = len(os.listdir(train_dir))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])



import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input

# Set hyperparameters
img_height = 224
img_width = 224
batch_size = 32
num_epochs = 10
num_classes = 2

# Create data generators for train and validation sets
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode='nearest')

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    '/content/gdrive/MyDrive/new kidney/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

val_generator = val_datagen.flow_from_directory(
    '/content/gdrive/MyDrive/new kidney/val',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

# Load the InceptionV3 model without the top layers
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))

# Add custom top layers for our dataset
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Combine the base model and the custom top layers
model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs=num_epochs,
    validation_data=val_generator,
    batch_size=batch_size,
    steps_per_epoch=train_generator.samples//batch_size,
    validation_steps=val_generator.samples//batch_size)

"""SAVING THE MODEL"""

model.save('/content/drive/MyDrive/kidneymodel/inception.h5')

"""when testing on new image...from class normal"""

from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input

img_height = 224
img_width = 224

# Load the image
img = image.load_img('/content/drive/MyDrive/kidney/Normal/Normal- (1002).jpg', target_size=(img_height, img_width))

# Preprocess the image
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# Make predictions
preds = model.predict(img)

print(preds)

"""So, in this case, the predicted class for the input image '/content/drive/MyDrive/kidney/Normal/Normal- (1002).jpg' would be a normal kidney, since the predicted probability (0.5074756) is lesser than the threshold of 0.5."""

from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input

img_height = 224
img_width = 224

# Load the image
img = image.load_img('/content/drive/MyDrive/kidney/Stone/Stone- (210).jpg', target_size=(img_height, img_width))

# Preprocess the image
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# Make predictions
preds = model.predict(img)

print(preds)

"""the probability is 0.52, which is greater than 0.5, which means the model predicts that the input image contains a kidney stone.

output with printing stone or not
"""

img_height = 224
img_width = 224

# Load the image
img = image.load_img('/content/drive/MyDrive/kidney/Stone/Stone- (1016).jpg', target_size=(img_height, img_width))

# Preprocess the image
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# Make predictions
preds = model.predict(img)

print(preds)
# Make predictions
preds = model.predict(img)

# Set a new threshold value
threshold = 0.5

# Classify the output probabilities based on the threshold
if preds > threshold:
    print("The input image contains a kidney stone.")
else:
    print("The input image contains a normal kidney.")

img_height = 224
img_width = 224

# Load the image
img = image.load_img('/content/drive/MyDrive/kidney/Normal/Normal- (1108).jpg', target_size=(img_height, img_width))

# Preprocess the image
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = preprocess_input(img)

# Make predictions
preds = model.predict(img)

print(preds)
# Make predictions
preds = model.predict(img)

# Set a new threshold value
threshold = 0.5

# Classify the output probabilities based on the threshold
if preds > threshold:
    print("The input image contains a kidney stone.")
else:
    print("The input image contains a normal kidney.")

