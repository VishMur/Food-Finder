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