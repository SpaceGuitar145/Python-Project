# import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import cv2
from keras import applications, Sequential, Model, optimizers
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.layers import Flatten, Dense
from keras.utils import to_categorical
from tqdm import tqdm
import os
import skimage.transform

trainInput = "chest-xray-pneumonia/chest_xray/chest_xray/train/"
testInput = "chest-xray-pneumonia/chest_xray/chest_xray/test/"
size = 199
batchSize = 32
epochs = 3


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
    return labels, images


labelsTrain, imagesTrain = extractData(trainInput)
labelsTest, imagesTest = extractData(testInput)

# imagesTrain = imagesTrain.reshape(5216, 3, size, size)
# imagesTest = imagesTest.reshape(624, 3, size, size)
# labelsTrain = to_categorical(labelsTrain, 2)
# labelsTest = to_categorical(labelsTest, 2)
print("Train:", imagesTrain.shape, "Test:", imagesTest.shape)
print("Train:", labelsTrain.shape, "Test:", labelsTest.shape)

inceptionv3 = applications.InceptionV3(weights='imagenet', include_top=False, input_shape=(size, size, 3))
addModel = Sequential()

addModel.add(Flatten(input_shape=inceptionv3.output_shape[1:]))
addModel.add(Dense(256, activation='relu'))
addModel.add(Dense(128, activation='relu'))
addModel.add(Dense(2, activation='softmax'))

modelv3 = Model(inputs=inceptionv3.input, outputs=addModel(inceptionv3.output))
modelv3.compile(loss='categorical_crossentropy', optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), metrics=['accuracy'])

# reduceLearningRate = ReduceLROnPlateau(monitor='val_acc', factor=0.1, epsilon=0.0001, patience=1, verbose=1)

reduceLearningRate = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=2, cooldown=2, min_lr=0.001, verbose=1)
earlyStop = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

callbacks = [reduceLearningRate, earlyStop]

timeStart = time.time()
history = modelv3.fit(imagesTrain, labelsTrain,
                      validation_data=(imagesTest, labelsTest),
                      callbacks=[reduceLearningRate, earlyStop], epochs=epochs)
print("InceptionV3 model", str(round((time.time() - timeStart) / 60, 2)))

"""History in graphs"""

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()

plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("Loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["Train", "Test"], loc="upper left")
plt.show()
