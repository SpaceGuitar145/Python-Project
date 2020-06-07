import numpy as np
import tensorflow as tf
import keras
from keras import models, backend
import os
import h5py
from PIL import Image
import matplotlib.pyplot as plt

try:
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
    tf.compat.v1.keras.backend.set_session(sess)
except:
    print("Can't use the graphic card. Not found.")

size = 199
epochs = 3
modelsDir = "/home/valera/pneumonia/models"


def global_test(modelsDir, dir_test_image):
    models_stat = []
    num_mod = 0

    labels = []
    images = []

    for nextDirectory in os.listdir(dir_test_image):
        if not nextDirectory.startswith("."):
            if nextDirectory in "NORMAL":
                label = 0
            elif nextDirectory in "PNEUMONIA":
                label = 1
            else:
                label = 2

            currentDirectory = dir_test_image + nextDirectory
            if not currentDirectory.startswith("."):
                for files in os.listdir(currentDirectory):
                    if files.endswith('.jpg') or files.endswith('.jpeg'):
                        imagePath = currentDirectory + "/" + files
                        img = Image.open(imagePath)
                        img = img.resize((size, size)).convert("RGB")
                        data = np.array(img.getdata())
                        img = 2 * (data.reshape((img.size[0], img.size[1], 3)).astype(np.float32) / 255) - 1
                        images.append(img)
                        labels.append(label)

    labels = np.asarray(labels)
    average_accuracy = [0] * len(labels)

    out = h5py.File("/home/valera/pneumonia/tmptest.h5", "a")
    out.create_dataset("imagesTmp", data=images)
    out.close()

    dset = h5py.File("/home/valera/pneumonia/tmptest.h5", "r")
    imagesTmp = dset["imagesTmp"][:]
    os.remove("/home/valera/pneumonia/tmptest.h5")

    for file_model in os.listdir(modelsDir):
        num_mod += 1

        model_name = modelsDir + "/" + file_model
        name = file_model[:-3]
        model_stat = [name]

        model = models.load_model(model_name)
        predictions = model.predict(imagesTmp, batch_size=1)
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

        model_stat.append(np.sum(accuracy_array) / len(accuracy_array) * 100)
        models_stat.append(model_stat)

    for i in range(len(average_accuracy)):
        average_accuracy[i] = average_accuracy[i] / num_mod
    models_stat.append(["Average", np.sum(average_accuracy) / len(average_accuracy) * 100])

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

    name_image = []
    images = []

    for files in os.listdir(dir_name):
        if files.endswith('.jpg') or files.endswith('.jpeg'):
            imagePath = dir_name + files
            name_image.append(files)
            img = Image.open(imagePath)
            img = img.resize((size, size)).convert("RGB")
            data = np.array(img.getdata())
            img = 2 * (data.reshape((img.size[0], img.size[1], 3)).astype(np.float32) / 255) - 1
            images.append(img)

    out = h5py.File("/home/valera/pneumonia/tmptest.h5", "a")
    out.create_dataset("imagesTmp", data=images)
    out.close()

    dset = h5py.File("/home/valera/pneumonia/tmptest.h5", "r")
    imagesTmp = dset["imagesTmp"][:]
    os.remove("/home/valera/pneumonia/tmptest.h5")

    for file_model in os.listdir(modelsDir):
        # print("==================================================\nCurrent model is: ", file_model)
        num_mod += 1
        model_name = modelsDir + "/" + file_model

        model = models.load_model(model_name)
        predictions = model.predict(imagesTmp, batch_size=1)
        predictions = predictions.reshape(1, -1)[0]

        accuracy_array = []

        for i in range(0, len(predictions), 2):
            accuracy_array.append(predictions[i + 1])
        images_stat.append(accuracy_array)
        # print(accuracy_array)
    result = []

    for i in range(len(name_image)):
        sum_ac = 0
        for j in range(num_mod):
            sum_ac += images_stat[j][i]
        result.append([name_image[i], sum_ac / num_mod * 100])
    return result

