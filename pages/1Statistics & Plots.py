import streamlit as st
from PIL import Image
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space


st.set_page_config(
    page_title="Statistics & Plots",
)

st.title("Statistics & Plots")
st.header("Relevant Graphs")

image = Image.open('img_assets/Food Insecurity in America.png')
st.image(image, caption='USDA 2018')