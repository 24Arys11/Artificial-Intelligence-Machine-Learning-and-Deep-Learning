import torch
from torchvision.transforms.functional import to_tensor, normalize

from sklearn import svm
from sklearn.metrics import accuracy_score

# import torchvision.models as models

# import statistics
# import numpy as np
# from sklearn import datasets

# import random
import cv2
import os

# from google.colab import files, auth, drive
# drive.mount('/content/drive')
# drive.mount('/content/gdrive')

DEBUG = True

# GETTING THE DATA IN "EASY-TO-WORK-WITH" FORMAT !!!

mean, std = 42.71899717948718, 47.51068434986272
# MEANS = []
# STDEVS = []

"""
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result
"""


class Organizer:

    def __init__(self, text_file, has_labels=True):
        self.link_dict = {}

        f = open(text_file, "r")
        content = f.read()

        rows = content.split("\n")

        for row in rows:
            if has_labels:
                values = row.split(",")
            else:
                values = [row, 0]
            if len(values) == 2:
                self.link_dict[values[0]] = values[1]

    def load_images(self, folder):  # , img_resize=30):
        images = []
        labels = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, filename), 0)
            # img = rotate_image(img, random.randint(0, 359))
            # mean, std = cv2.meanStdDev(img)
            # MEANS.append(float(mean))
            # STDEVS.append(float(std))
            img = normalize(to_tensor(img), [mean], [std])
            if img is not None:
                images.append(img)
                labels.append(int(self.link_dict[filename]))
        return torch.unsqueeze(torch.cat(images, dim=0), dim=1).reshape(-1, 2500), torch.Tensor(labels)

    def submit(self, filename, labels):
        f = open(filename, "w")
        output_content = "id,label\n"
        for idx, key in enumerate(self.link_dict.keys()):
            if idx < len(labels):
                output_content += key
                output_content += ","
                output_content += str(labels[idx])
                output_content += "\n"
        f.write(output_content)


if DEBUG:
    print("Incepem incarcarea imaginilor de train")
training_data = Organizer("data/train.txt")
X_train, y_train = training_data.load_images("data/train/")

if DEBUG:
    print("Done. Incepem incarcarea imaginilor de validare")
validation_data = Organizer("data/validation.txt")
X_validation, y_validation = validation_data.load_images("data/validation/")

if DEBUG:
    print("Done. Incepem incarcarea imaginilor de test")
testing_data = Organizer("data/test.txt", has_labels=False)
X_test, zeroes = testing_data.load_images("data/test/")
if DEBUG:
    print("Done")


def predict(model):

    f = open("data/test.txt", "r")
    content = f.read()

    img_names = content.split("\n")

    images = []

    for name in img_names:
        if name != "":
            img = cv2.imread(os.path.join("data/test/", name), 0)
            img = torch.unsqueeze(normalize(to_tensor(img), [mean], [std]), dim=0)
            images.append(img)

    predictions = []
    with torch.no_grad():
        for image in images:
            label = int(model.predict(image.reshape(-1, 2500)))
            predictions.append(label)
    return predictions


# print(f"Mean: {statistics.mean(MEANS)}; STD: {statistics.mean(STDEVS)}")

# network.load_state_dict(torch.load("best_model.pth"))
# train_fn(args.epochs, train_loader, valid_loader, network, loss_fn, optimizer)

# my_model = Network().to(device)
# my_model.load_state_dict(torch.load("VGG16.pth"))

print("Creating model...")
svm_model = svm.SVC(C=1)

print("Training model...")
svm_model.fit(X_train, y_train)

print("Done. Calculating accuracy...")
acc = accuracy_score(y_validation, svm_model.predict(X_validation))

print(f"Acuratetea calculata este {acc * 100}%")

# X, y = datasets.make_blobs(n_samples=50, n_features=2, centers=2, cluster_std=1.05, random_state=40)

preds = predict(svm_model)
"""
print(f"X_train.shape: {X_train.shape}, y_train.shape: {y_train.shape}")
print(f"X_validation.shape: {X_validation.shape}, y_validation.shape: {y_validation.shape}")
print(f"X_test.shape: {X_test.shape}, preds.shape: {preds.shape}")
"""
testing_data.submit("submisions.txt", preds)

if DEBUG:
    print("Submisions successfully saved in submisions.txt !")
