# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import cv2
from keras import applications, Sequential, Model, optimizers
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.layers import Flatten, Dense
from tqdm import tqdm
import os
import skimage.transform

# Using model inception v3, cause its made to differ images
trainInput = "chest-xray-pneumonia/chest_xray/chest_xray/train/"
testInput = "chest-xray-pneumonia/chest_xray/chest_xray/test/"
size = 199

def extractData(directory):
    labels = []
    images = []

    for nextDirectory in os.listdir(directory):
        if not nextDirectory.startswith("."):
            if nextDirectory in "NORMAL":
                label = 0
            elif nextDirectory in "PNEUMONIA":
                label = 1
            else:
                label = 2

            currentDirectory = directory + nextDirectory
            if not currentDirectory.startswith("."):
                for files in tqdm(os.listdir(currentDirectory)):
                    if files.endswith('.jpg') or files.endswith('.jpeg'):
                        imagePath = currentDirectory + "/" + files
                        img = cv2.imread(imagePath)
                        img = skimage.transform.resize(img, (size, size, 3))
                        img = np.asarray(img)
                        labels.append(label)
                        images.append(img)
                        # cv2.imshow('image', img)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

    labels = np.asarray(labels)
    images = np.asarray(images)
    return images, labels


imagesTrain, labelsTrain = extractData(trainInput)
imagesTest, labelsTest = extractData(testInput)


inceptionv3 = applications.InceptionV3(weights='imagenet', include_top=False, input_shape=(size, size, 3))
addModel = Sequential()

addModel.add(Flatten(input_shape=inceptionv3.output_shape[1:]))
addModel.add(Dense(256, activation='relu'))
addModel.add(Dense(128, activation='relu'))
addModel.add(Dense(2, activation='softmax'))

modelv3 = Model(inputs=inceptionv3.input, outputs=addModel(inceptionv3.output))
modelv3.compile(loss='categorical_crossentropy', optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), metrics=['accuracy'])
