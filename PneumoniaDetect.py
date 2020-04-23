# import pandas as pd
# import keras
# import torch
import numpy as np
import cv2
import os
import skimage.transform
# Using model inception v3, cause its made to differ images
trainInput = "chest-xray-pneumonia/chest_xray/chest_xray/train/"
testInput = "chest-xray-pneumonia/chest_xray/chest_xray/test/"
tst = "/home/push/Desktop"

print(os.listdir(trainInput))


def createLabel():
    for nextdir in os.listdir(trainInput):
        if nextdir in "NORMAL":
            label = 0
        elif nextdir in "PNEUMONIA":
            label = 1
        else:
            label = 2


print(os.listdir(tst))


# Test working of image reader, to view next image, press esc
# Later will be change to readImage (comment from cv2.imshow() )
def showImage(directory):
    for files in os.listdir(directory):
        if files.endswith('.jpg') or files.endswith('.jpeg'):
            imagePath = directory + "/" + files
            img = cv2.imread(imagePath)
            img = skimage.transform.resize(img, (299, 299, 3))
            print(img)
            img = np.asarray(img)
            print(img)


showImage(tst)
