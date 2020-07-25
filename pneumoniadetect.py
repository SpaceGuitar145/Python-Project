import numpy as np
import tensorflow as tf
from PIL import Image
from keras import models, backend
import os
import matplotlib.pyplot as plt

try:
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
    tf.compat.v1.keras.backend.set_session(sess)
except:
    print("Can't use the graphic card. Not found.")

size = 199
modelsDir = "pneumonia/models/"


def processingImage(directory):
    images, imageTitles, labels = [], [], []
    for nextDirectory in os.listdir(directory):
        if not nextDirectory.startswith("."):
            print("next dir", nextDirectory)
            if nextDirectory in "NORMAL":
                label = 0
            elif nextDirectory in "PNEUMONIA":
                label = 1
            else:
                label = 2

            currentDirectory = directory + nextDirectory
            dirs = directory
            if currentDirectory.endswith(".jpg") or currentDirectory.endswith(".jpeg"):
                print("Dir1", dirs)
            else:
                dirs = currentDirectory
                print("Dir2", dirs)

            for files in os.listdir(dirs):
                if files.endswith(".jpg") or files.endswith(".jpeg"):
                    imagePath = dirs + "/" + files
                    imageTitles.append(files)

                    img = Image.open(imagePath)
                    img = img.resize((size, size)).convert("RGB")
                    data = np.array(img.getdata())
                    img = 2 * (data.reshape((img.size[0], img.size[1], 3)) / 255) - 1
                    images.append(img)
                    labels.append(label)
                else:
                    print("No such file extension")
            if currentDirectory.endswith(".jpg") or currentDirectory.endswith(".jpeg"):
                break

    images = np.asarray(images)
    labels = np.asarray(labels)
    return imageTitles, images, labels


def global_test(modelsDir, dir_test_image):
    models_stat = []
    num_mod = 0

    _, images, labels = processingImage(dir_test_image)

    average_accuracy = [0] * len(labels)

    for file_model in os.listdir(modelsDir):
        num_mod += 1

        model_name = modelsDir + "/" + file_model
        name = file_model[:-3]
        model_stat = [name]

        model = models.load_model(model_name)
        predictions = model.predict(images, batch_size=1)
        predictions = predictions.reshape(1, -1)[0]

        accuracy_array = []

        x = -1
        for i in range(0, len(predictions), 2):
            x += 1
            if predictions[i] > predictions[i + 1]:
                if labels[x] == 0:
                    accuracy_array.append(predictions[i])
                    average_accuracy[x] += predictions[i]
                else:
                    accuracy_array.append(predictions[i + 1])
                    average_accuracy[x] += predictions[i + 1]

            if predictions[i] < predictions[i + 1]:
                if labels[x] == 1:
                    accuracy_array.append(predictions[i + 1])
                    average_accuracy[x] += predictions[i + 1]
                else:
                    accuracy_array.append(predictions[i])
                    average_accuracy[x] += predictions[i]

        model_stat.append(np.mean(accuracy_array) * 100)
        models_stat.append(model_stat)

    models_stat.append(["Average", np.mean(average_accuracy) / num_mod * 100])

    x_data = []
    y_data = []
    for i in range(len(models_stat)):
        x_data.append(models_stat[i][0])
        y_data.append(models_stat[i][1])
    _, ax = plt.subplots()
    ax.bar(x_data, y_data, color='#539caf', align='center')
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Models")
    plt.savefig("test_stat.png")


def global_predict(modelsDir, dir_name):
    images_stat = []
    num_mod = 0

    imageTitles, images, _ = processingImage(dir_name)

    for file_model in os.listdir(modelsDir):
        num_mod += 1
        model_name = modelsDir + "/" + file_model

        model = models.load_model(model_name)
        predictions = model.predict(images, batch_size=1)
        predictions = predictions.reshape(1, -1)[0]

        accuracy_array = []

        for i in range(0, len(predictions), 2):
            accuracy_array.append(predictions[i + 1])
        images_stat.append(accuracy_array)

    result = []
    for i in range(len(imageTitles)):
        result.append([imageTitles[i], np.mean([images_stat[k][i] for k in range(len(images_stat))]) * 100])
    return result


print(global_predict("/home/push/Documents/GitHub/Python-Project-Pneumonia-Detect/pneumonia/models/",
                     "/home/push/Documents/GitHub/Python-Project-Pneumonia-Detect/pneumonia/predict/"))
