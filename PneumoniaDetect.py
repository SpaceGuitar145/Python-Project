# import pandas as pd
# import keras
# import torch
# import numpy as np
import cv2
import os


trainInput = "chest-xray-pneumonia/chest_xray/chest_xray/train/"
testInput = "chest-xray-pneumonia/chest_xray/chest_xray/test/"
tst = "/home/push/Desktop"

print(os.listdir(trainInput))

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
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


showImage(tst)
