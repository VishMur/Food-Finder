import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import torch
import torchvision
from torchvision import transforms, datasets, models
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from PIL import Image
import random
from sklearn.metrics import confusion_matrix
import itertools
import os

st.set_page_config(
    page_title="Fruit Classifier",
)

st.title("Fruit Classifier")
st.header("Image class predictor")
st.write(
    """This classifier will attempt to identify the fruit and the quality with high accuracy.
     Click on one of the three example files to see the classifier in action, or upload your own
     image (in JPG, PNG, or JPEG form). Enjoy!"""
)

classes = ('Acceptable_Apple', 'Acceptable_Banana', 'Acceptable_Guava', 'Acceptable_Lemon',
           'Acceptable_Orange', 'Acceptable_Pomegranate', 'Bad_Apple', 'Bad_Banana', 'Bad_Guava',
           'Bad_Lemon', 'Bad_Orange', 'Bad_Pomegranate', 'Good_Apple', 'Good_Banana', 'Good_Guava',
           'Good_Lemon', 'Good_Orange', 'Good_Pomegranate')

width_mean = 300
height_mean = 300

transform = transforms.Compose([transforms.Resize((width_mean, height_mean)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5), (0.5))])

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # For first number, use 1 for B/W images, use 3 for color images
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(5, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.do1 = nn.Dropout(0.4)
        self.do2 = nn.Dropout(0.3)
        self.fc1 = nn.Linear(1936, 512)
        self.fc2 = nn.Linear(512, 64)
        self.fc3 = nn.Linear(64, 18)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = self.do1(x)
        x = F.relu(self.fc1(x))
        x = self.do1(x)
        x = F.relu(self.fc2(x))
        x = self.do2(x)
        x = self.fc3(x)
        return x

net = Net()

def main():
    page_names = ('Own Data', 'Example 1', 'Example 2', 'Example 3')
    page = st.radio('Image Examples', page_names)
    if page == 'Own Data':
        file_uploaded = st.file_uploader("Choose the file", type=['jpg', 'png', 'jpeg'])
        st.info('Upload an image!')
        if file_uploaded is not None:
            image = Image.open(file_uploaded)
            figure = plt.figure()
            plt.grid(False)
            plt.axis('off')
            plt.imshow(image)
            result = predict_class(image)
            st.write("Class Prediction: " + result)
            st.pyplot(figure)
    elif page == 'Example 1':
        image = Image.open('ml_example_images/good_orange_example.png')
        figure = plt.figure()
        plt.grid(False)
        plt.axis('off')
        plt.imshow(image)
        result = predict_class(image)
        st.write("Class Prediction: " + result)
        st.pyplot(figure)
    elif page == 'Example 2':
        image = Image.open('ml_example_images/acceptable_banana_example.png')
        figure = plt.figure()
        plt.grid(False)
        plt.axis('off')
        plt.imshow(image)
        result = predict_class(image)
        st.write("Class Prediction: " + result)
        st.pyplot(figure)
    elif page == 'Example 3':
        image = Image.open('ml_example_images/bad_apple_example.png')
        figure = plt.figure()
        plt.grid(False)
        plt.axis('off')
        plt.imshow(image)
        result = predict_class(image)
        st.write("Class Prediction: " + result)
        st.pyplot(figure)

weight = "eda_ml_notebooks/weights.pt"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def predict_class(image):
    model = Net()
    model.load_state_dict(torch.load(weight))
    image = transform(image).float()
    image = image.unsqueeze_(0)
    image = image.to(device)
    with torch.no_grad():
        model.eval()
        output = model(image)
        # print(output)
        index = output.data.cpu().numpy().argmax()
        class_name = classes[index]
        return class_name
    print('This fruit is: ', ' '.join(f'{class_name}'))

if __name__ == "__main__":
    main()