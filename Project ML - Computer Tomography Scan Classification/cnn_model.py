import torch
from torch import nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision.transforms.functional import to_tensor, normalize

# import statistics
import numpy as np

import random
import cv2
import os

# from google.colab import files, auth, drive
# drive.mount('/content/drive')
# drive.mount('/content/gdrive')

DEBUG = True

# GETTING THE DATA IN "EASY-TO-WORK-WITH" FORMAT !!!
kwargs = {}


class Args:

    def __init__(self):
        self.batch_size = 64
        self.epochs = 20
        self.lr = 0.00001
        self.seed = 1


args = Args()

mean, std = 42.71899717948718, 47.51068434986272
# MEANS = []
# STDEVS = []

use_cuda = torch.cuda.is_available()
torch.manual_seed(args.seed)
device = torch.device("cuda" if use_cuda else "cpu")

if DEBUG:
    print(f"use_cuda = {use_cuda}")
kwargs = {'num_workers': 0, 'pin_memory': True} if use_cuda else {}


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


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

    def load_images(self, folder):  #, img_resize=30):
        images = []
        labels = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, filename), 0)
            img = rotate_image(img, random.randint(0, 359))
            # mean, std = cv2.meanStdDev(img)
            # MEANS.append(float(mean))
            # STDEVS.append(float(std))
            img = normalize(to_tensor(img), [mean], [std])
            if img is not None:
                images.append(img)
                labels.append(int(self.link_dict[filename]))
        return torch.unsqueeze(torch.cat(images, dim=0), dim=1), torch.Tensor(labels)

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


class MyDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):

        return self.x[idx], self.y[idx]


variations = args.epochs
if DEBUG:
    print(f"We aim to create {variations} variations")
training_set = []
for idx in range(variations):
    X_train, y_train = training_data.load_images("data/train/")
    ts = MyDataset(X_train, y_train)
    training_set.append(ts)
    if DEBUG:
        print("{:.1f}%".format((idx * 100) / variations), end=" ")
if DEBUG:
    print("100%")

validation_set = MyDataset(X_validation, y_validation)

testing_set = MyDataset(X_test, zeroes)

if DEBUG:
    print("Facem data loaderele")
train_loaders = []
for idx, ts in enumerate(training_set):
    train_loader = DataLoader(dataset=ts, batch_size=args.batch_size, shuffle=False, **kwargs)
    train_loaders.append(train_loader)
    if DEBUG:
        print("{:.1f}%".format((idx * 100) / variations), end=" ")
if DEBUG:
    print("100%")
if DEBUG:
    print(f"We created {len(training_set)} train_loader variations !")

valid_loader = DataLoader(dataset=validation_set, batch_size=1, shuffle=False, **kwargs)

test_loader = DataLoader(dataset=testing_set, batch_size=1, shuffle=False, **kwargs)
if DEBUG:
    print("Done")

channels_conv1 = 512
channels_conv2 = 256
channels_conv3 = 256
connection = 4096
features_fc1 = 1024
features_fc2 = 1024
features_fc3 = 512
dropout_features = 0.15
dropout_weights = 0.2


class Network(nn.Module):

    def __init__(self):
        super().__init__()
        self.layer1 = nn.Conv2d(in_channels=1, out_channels=channels_conv1, kernel_size=(5, 5), stride=(1, 1))
        self.layer2 = nn.Conv2d(in_channels=channels_conv1, out_channels=channels_conv2, kernel_size=(5, 5), stride=(1, 1), padding=(1, 1))
        self.layer3 = nn.Conv2d(in_channels=channels_conv2, out_channels=channels_conv3, kernel_size=(5, 5), stride=(1, 1), padding=(1, 1))

        self.linear1 = nn.Linear(connection, features_fc1)
        self.linear2 = nn.Linear(features_fc1, features_fc2)
        self.linear3 = nn.Linear(features_fc2, features_fc3)
        self.linear4 = nn.Linear(features_fc3, 3)

        self.norm1 = nn.BatchNorm2d(channels_conv1)
        self.norm2 = nn.BatchNorm2d(channels_conv2)
        self.norm3 = nn.BatchNorm2d(channels_conv3)

        self.flatten = nn.Flatten()
        self.softmax = nn.Softmax(dim=1)
        self.maxPool = nn.MaxPool2d(2, 2)
        self.avgPool = nn.AvgPool2d(2, 2)
        self.dropout_features = nn.Dropout(dropout_features)
        self.dropout_weights = nn.Dropout(dropout_weights)

    def forward(self, output):
        output = F.relu(self.norm1(self.maxPool(self.layer1(output))))
        output = self.dropout_features(output)
        output = F.relu(self.norm2(self.maxPool(self.layer2(output))))
        output = self.dropout_features(output)
        output = F.relu(self.norm3(self.maxPool(self.layer3(output))))
        output = self.dropout_features(output)

        output = self.flatten(output)
        # print(output.shape)
        output = self.linear1(output)
        output = self.dropout_weights(output)
        output = self.linear2(output)
        output = self.dropout_weights(output)
        output = self.linear3(output)
        output = self.dropout_weights(output)
        output = self.linear4(output)
        output = self.softmax(output)

        return output


# Definirea retelei
network = Network().to(device)

# Definirea Optimizatorului
optimizer = optim.Adam(network.parameters(), lr=args.lr)
optimizer.zero_grad()

# Definirea functiei de cost pentru clasificare
loss_fn = nn.CrossEntropyLoss()


def train_fn(epochs: int, train_loader: DataLoader, validation_loader: DataLoader, model: nn.Module, loss_fn: nn.Module, optimizer: optim.Optimizer):

    max_acc = 65
    if DEBUG:
        print("Begin training...")
    for epoch in range(epochs):
        model.dropout_features = nn.Dropout(dropout_features)
        model.dropout_weights = nn.Dropout(dropout_weights)
    # Iteram prin fiecare exemplu din dataset
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device).long()
          # Aplicam reteaua neurala pe imaginile de intrare
            out = model(images)
          # Aplicam functia cost pe iesirea retelei neurale si pe adnotarile imaginilor
            loss = loss_fn(out, labels)
          # Aplicam algoritmul de back-propagation
            loss.backward()
          # Facem pasul de optimizare, pentru a aplica gradientii pe parametrii retelei
            optimizer.step()
          # Apelam functia zero_grad() pentru a uita gradientii de la iteratie curenta
            optimizer.zero_grad()

        print(f"Loss-ul dupa epoca {epoch + 1} este {loss.item()}")

         # Caluculul acuratetii
        model.dropout_features = nn.Dropout(0)
        model.dropout_weights = nn.Dropout(0)
        count = len(validation_loader)
        correct = 0
        model.eval()
        with torch.no_grad():
            for val_image, val_label in validation_loader:
                if use_cuda:
                    val_label = val_label.cuda()
                    val_image = val_image.cuda()
                    out_class = torch.argmax(model(val_image))
                if out_class == val_label:
                    correct += 1

        current_acc = (correct / count) * 100
        print(f"Acuratetea dupa epoca {epoch + 1} este {current_acc}%")
        if current_acc > max_acc:
            max_acc = current_acc
            torch.save(model.state_dict(), "best_model.pth")
    if DEBUG:
        print(f"Max accuracy obtained: {max_acc}")


def predict(model: nn.Module):

    f = open("data/test.txt", "r")
    content = f.read()

    img_names = content.split("\n")

    images = []

    for name in img_names:
        if name != "":
            img = cv2.imread(os.path.join("data/test/", name), 0)
            img = torch.unsqueeze(normalize(to_tensor(img), [mean], [std]), dim=0)
            images.append(img)

    model.dropout_features = nn.Dropout(0)
    model.dropout_weights = nn.Dropout(0)
    predictions = []
    with torch.no_grad():
        for image in images:
            if use_cuda:
                image = image.cuda()
            label = torch.argmax(model(image))
            label = label.detach().cpu().numpy()
            predictions.append(label)
    return predictions


# print(f"Mean: {statistics.mean(MEANS)}; STD: {statistics.mean(STDEVS)}")

network.load_state_dict(torch.load("best_model.pth"))
train_fn(args.epochs, train_loader, valid_loader, network, loss_fn, optimizer)

my_model = Network().to(device)
my_model.load_state_dict(torch.load("best_model.pth"))

preds = predict(my_model)

testing_data.submit("submisions.txt", preds)

if DEBUG:
    print("Submisions successfully saved in submisions.txt !")
