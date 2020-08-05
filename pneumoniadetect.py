import numpy as np
import tensorflow as tf
from PIL import Image
from keras import models
import os
import matplotlib.pyplot as plt

size = 199
modelsDir = os.getcwd() + "/pneumonia/models/"

# todo train DenseNet201, VGG16, InceptionResNetV2, Xception

try:
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
    tf.compat.v1.keras.backend.set_session(sess)
except Exception as e:
    print("Can't use the graphics card. Not found. Exc: ", e)


class PneumoniaDetect:
    def __init__(self, modelsDirectory, inputDirectory):
        self.modelsDirectory = modelsDirectory
        self.inputDirectory = inputDirectory
        self.images = []
        self.imageTitles = []
        self.labels = []

    def processingImage(self, directory):
        imagesTmp, labelsTmp = [], []
        for nextDirectory in os.listdir(directory):
            if not nextDirectory.startswith("."):
                if nextDirectory in "NORMAL":
                    label = 0
                elif nextDirectory in "PNEUMONIA":
                    label = 1
                else:
                    label = 2

                currentDirectory = directory + nextDirectory
                dirs = directory

                if currentDirectory.endswith(".jpg") or currentDirectory.endswith(".jpeg"):
                    pass
                else:
                    dirs = currentDirectory

                for files in os.listdir(dirs):
                    if files.endswith(".jpg") or files.endswith(".jpeg"):
                        imagePath = dirs + "/" + files
                        self.imageTitles.append(files)

                        img = Image.open(imagePath)
                        img = img.resize((size, size)).convert("RGB")
                        data = np.array(img.getdata())
                        img = 2 * (data.reshape((img.size[0], img.size[1], 3)) / 255) - 1
                        imagesTmp.append(img)
                        labelsTmp.append(label)
                    else:
                        print("No such file extension allowed")
                if currentDirectory.endswith(".jpg") or currentDirectory.endswith(".jpeg"):
                    break

        self.images = np.asarray(imagesTmp)
        self.labels = np.asarray(labelsTmp)

    def modelsTest(self):
        modelStat = {}
        self.processingImage(self.inputDirectory)

        for modelPath in os.listdir(self.modelsDirectory):
            dirModel = self.modelsDirectory + modelPath
            name = modelPath.split(".")[0]
            model = models.load_model(dirModel)
            predictions = model.predict(self.images)
            accuracy = 0
            for i in range(len(predictions)):
                if self.labels[i] == np.argmax(predictions[i]):
                    accuracy += 1
            modelStat[name] = accuracy / len(predictions) * 100

        # for key, value in modelStat.items():
        #     print(f"Model is {key}\nAccuracy of predictions is: {value}%")

        _, ax = plt.subplots()
        ax.bar(modelStat.keys(), modelStat.values(), color="#539caf", align="center")
        ax.set_ylabel("Accuracy")
        ax.set_xlabel("Models")
        plt.savefig("test_stat.png")

    def modelsPrediction(self):
        imagesStat = {}

        self.processingImage(self.inputDirectory)

        for modelPath in os.listdir(self.modelsDirectory):
            dirModel = self.modelsDirectory + modelPath
            model = models.load_model(dirModel)
            predictions = model.predict(self.images, batch_size=1)

            for i in range(len(predictions)):
                if self.imageTitles[i] not in imagesStat:
                    imagesStat[self.imageTitles[i]] = []
                imagesStat[self.imageTitles[i]].append(predictions[i][1])

        for i in imagesStat:
            imagesStat[i] = np.mean(imagesStat[i]) * 100

        return imagesStat


# pd = PneumoniaDetect(os.getcwd()+"/pneumonia/models/", os.getcwd()+"/pneumonia/predict/")
# print(pd.modelsPrediction())
