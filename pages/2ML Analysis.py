import streamlit as st
import time
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Data and Machine Learning Analysis",)

st.title("Data and Machine Learning Analysis")
st.markdown("This page contains information about the data used and the machine learning model the Food Finder development team made to classify it.")
st.markdown("""     
       The model was 95.76% accurate at classifying produce (fruit) into the following categories: 
       - fruit quality: good, acceptable/ugly, bad
       - fruit type: apple, banana, guava, orange, lemon, pomegranate
"""
)
add_vertical_space(1)

st.header("Data Visualizations Analysis")

st.write(
    """Because the data is in the form of images, it was hard to compare different classes on a graph
       (such as, for example, a box and whisker plot showing the distribution of data). However, it was
       possible to analyze how balanced the data classes are (how many of each type and quality of produce
       are present in the data).
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
add_vertical_space(1)

st.image("img_assets/ml analysis assets/fruit_type_counts.png")
st.write(
    """The data is primarily made of pomegranate pictures, but there is
      enough data from the other 5 types of fruit to distinguish between the 6 total classes of fruit type.
"""
)
add_vertical_space(1)

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
    
    1. Convolutional Layers
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
add_vertical_space(1)

# Image (Training Data) Picture - explain how split_folder library stratifies data split
st.image("img_assets/ml analysis assets/fruit_image_grid.png")
st.markdown("""
This grid shows 64 sample training images that were used to develop the model described above. 
- Data splits between the training and testing datasets were stratified (splits were made in a way that tried to balance the various fruit quality and
type classes). This prevented the model from over-training on a particular fruit type of quality, and increased its accuracy.
"""
)
add_vertical_space(1)

col1, col2 = st.columns(2)

with col1:
    st.image("img_assets/ml analysis assets/loss_by_epoch.png")
with col2:
    st.image("img_assets/ml analysis assets/accuracy_by_epoch.png")

st.markdown("""
The graphs above show that as the model learns from examples over time (epochs), the loss (prediction errors) decreases while the prediction accuracy
increases for both training and validation (unseen examples used to finetune the model) datasets. 

- Positive signs: These indicators show that the model got better at avoiding prediction errors, making accurate predictions, and handling
new/unseen data.
"""
)
add_vertical_space(1)

st.image("img_assets/ml analysis assets/confusion_matrix.png")
st.markdown("""
This confusion matrix provides a holistic view of the performance of the model on the test data by visualizing which categories the model is good
at and which ones it struggles with classifying. 

- The diagonal from the top left of the picture to the bottom right is almost universally shaded dark blue
    - The model classified the 18 of the image correctly, for the most part. The two categories it struggled with the most were the acceptable guavas
    and acceptable lemons, achieving a 71 and 76 percent accuracy on classifying them, respectively.
"""
)