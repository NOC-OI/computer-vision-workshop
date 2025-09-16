import copy
import os
import time
import sys

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from torch.optim import lr_scheduler
from torch.utils.data import RandomSampler
from torchvision import datasets, models, transforms
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Resize, ToTensor
from tqdm.notebook import tqdm, trange

sys.path.insert(1, os.path.join(os.getcwd(),'computer-vision-workshop/utilities'))
from display_utils import imshow_tensor, make_confmat
from split import stratified_random_split

TRAINING_PATH = "/groups/cv-workshop/ZooScan/train"
VALIDATION_PATH = "/groups/cv-workshop/ZooScan/train"


transform = Compose([
    # Resize every image to a 224x244 square
    Resize((224,224)),
    # Convert to a tensor that PyTorch can work with
    ToTensor()
])

# Images are located at at {dataset_path}/{class_name}/{objid}.jpg
dataset_train = ImageFolder(TRAINING_PATH, transform)
dataset_val = ImageFolder(TRAINING_PATH, transform)

# Make sure that the class names are identical
assert dataset_train.classes == dataset_val.classes

# Extract the tensor and the label of the first example
tensor, label = dataset_train[0]

print("Class: {:d} ({})".format(label, dataset_train.classes[label]))

model = models.resnet18(pretrained=True)

# get the number of features that are input to the fully connected layer
num_ftrs = model.fc.in_features

# reset the fully connect layer
model.fc = nn.Linear(num_ftrs, len(dataset_train.classes))

# Transfer model to GPU
model = model.cuda()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

loader_train = torch.utils.data.DataLoader(dataset_train, batch_size=128,
                                           shuffle=True, num_workers=2)

# Activate training mode
model.train()

# Train for 5 epochs
for epoch in trange(5, desc="Epoch"):
    # tqdm_notebook displays a nice progress bar
    with tqdm(loader_train, desc="Training Epoch #{:d}".format(epoch + 1)) as t:
        for inputs, labels in t:
            # Copy data to GPU
            inputs = inputs.cuda()
            labels = labels.cuda()
    # for ii, data in enumerate(loader_train, 0):
    #     inputs, labels = data
    #     inputs = inputs.cuda()
    #     labels = labels.cuda()
            # zero the parameter gradients
            optimizer.zero_grad()
    
            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
            # print statistics
            t.set_postfix(loss=loss.item())

print('Finished Training')
