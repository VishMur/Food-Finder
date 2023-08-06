import streamlit as st
import time
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Data and Machine Learning Analysis",)

st.title("Data and Machine Learning Analysis")
st.header("Data Visualizations Analysis")

st.write(
    """Because the data is in the form of images, it was hard to compare different classes on a graph
       (such as, for example, a box and whisker plot showing the distribution of data). However, it was
       possible to analyze how balanced the data classes are (how many of each type and quality of produce
       are shown).
"""
)

add_vertical_space(1)

st.image("img_assets/ml analysis assets/fruit_quality_counts.png")
st.write(
    """The data is overwhelmingly composed of good quality fruit, but there is
     still enough data for the ugly (acceptable) and bad fruit classes to train a machine learning classifier to
      distinguish between the 3 classes of fruit quality.
"""
)

st.image("img_assets/ml analysis assets/fruit_type_counts.png")
st.write(
    """The data is primarily made of pomegranate pictures, but there is
      enough data from the other 5 types of fruit to distinguish between the 6 total classes of fruit type.
"""
)

st.image("img_assets/ml analysis assets/fruit_quality_and_type_counts.png")
st.write(
    """This graph aggregates the information from the previous two graphs with both fruit type and quality. 
       A disproportionate percentage of bananas and lemons are ugly/acceptable fruit, and a disproportionate
      percentage of pomegranates are good fruit.
"""
)

add_vertical_space(1)

st.header("Machine Learning Visualizations Analysis")

st.write("The following section will present and analyze the machine learning architecture, process, and results")

add_vertical_space(1)

# Picture of Model
st.image("img_assets/ml analysis assets/model_visualization.png")
st.write(
    """
    Imagine a machine learning architecture as a set of instructions for a computer to learn from examples. Just like how we learn
    by looking at things, a machine learning model also "looks" at data to understand patterns and make decisions. In this case,
    our architecture is like a virtual brain called "Net." It's designed to recognize and categorize images, like distinguishing
    between different animals or objects in pictures.The first part of our architecture involves "convolutional" layers. These
    layers are like filters that help the model see important features in the images. Think of them as virtual glasses that
    highlight specific shapes or colors. The architecture has two of these layers: "conv1" and "conv2." Next, we have a special
    operation called "pooling." This operation helps the model focus on the most important information and reduce the complexity
    of the image. It's like zooming out to see the bigger picture. The architecture uses the "pool" function for this. After that,
    we have two "fully connected" layers: "fc1" and "fc2." These layers are like decision-makers that analyze the information
    gathered from the previous layers and make predictions about what the image might contain. However, we also want our model to
    be flexible and avoid becoming too rigid. To achieve this, we introduce "dropout" layers (do1 and do2). These layers randomly
    drop some of the connections in the model during training, forcing it to rely on other pathways and preventing overfitting
    (memorizing instead of learning). Finally, we have the last "fully connected" layer, "fc3," which is like the final
    decision-maker. It takes all the information gathered and predicts which category the image belongs to (e.g., a specific
    animal or object). Our architecture is designed to categorize images into 18 different classes. Once all these components
    are set up, we feed the images into the architecture, and it starts learning from the examples we provide. The more examples
    it sees, the better it becomes at recognizing and classifying images correctly. In summary, our machine learning architecture,
    "Net," is like a powerful image recognition brain. It looks at images through convolutional and pooling layers, analyzes the
    information with fully connected layers, stays flexible with dropout layers, and finally makes decisions about the image's
    category using the last fully connected layer. It learns from examples, becoming smarter with more practice.
"""
)

# Image (Training Data) Picture - explain how split_folder library stratifies data split