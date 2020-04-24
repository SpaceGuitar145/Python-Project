# import pandas as pd
# import keras
# import torch
# import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import skimage.transform

# Using model inception v3, cause its made to differ images
trainInput = "chest-xray-pneumonia/chest_xray/chest_xray/train/"
testInput = "chest-xray-pneumonia/chest_xray/chest_xray/test/"
tst = "/home/push/Desktop"


def extractData(directory):
    labels = []
    images = []

    def createLabel(directory):
        for nextdir in os.listdir(directory):
            if nextdir in "NORMAL":
                label = 0
            elif nextdir in "PNEUMONIA":
                label = 1
            else:
                label = 2
            print(label)
            labels.append(label)

    def showImage(directory):
        for files in os.listdir(directory):
            if files.endswith('.jpg') or files.endswith('.jpeg'):
                imagePath = directory + "/" + files
                img = cv2.imread(imagePath)
                img = skimage.transform.resize(img, (299, 299, 3))
                img = np.asarray(img)
                images.append(img)
                # cv2.imshow('image', img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    createLabel(directory)
    labels = np.asarray(labels)
    showImage(directory)
    images = np.asarray(images)
    return images, labels


imagesTrain, labelsTrain = extractData(trainInput)
# imagesTest, labelsTest = extractData(testInput)

