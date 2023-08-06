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
st.markdown(
    """
    The above image is a picture of our machine learning model architecture, a path of instructions for a computer to learn from examples.
    It's designed to recognize and categorize the 18 categories of images (6 types of fruit X 3 qualities of fruit).
    The following list shows the model components in order of how data is passed through it:
    
    1. Convolutional Layers. 
         - These layers are like filters that help the model see important features in the images
         - They highlight specific shapes or colors
         - 2 Convolutional layers are present 
    
    2. Pooling
         - This operation helps the model focus on the most important information and reduce the complexity of the image.
    
    3. "Fully Connected" Layers: 
         - These layers are like decision-makers that analyze the information.
         - They gather information from the previous layers and make predictions about what the image might contain. 
         - 2 Fully Connected layers are present
    
    4. "Dropout" Layers:
         - These layers randomly drop some of the connections in the model during training, forcing it to rely on other pathways and preventing overfitting (memorizing training data instead of learning)
         - 2 Dropout layers are present
    
    5. Final "Fully Connected" Layer:
         - It takes all the information gathered and predicts which category the image belongs to (1 of the 18 categroies mentioned above)
"""
)

# Image (Training Data) Picture - explain how split_folder library stratifies data split