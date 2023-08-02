"""
ScatterplotLayer
================

Plot of the number of exits for various subway stops within San Francisco, California.

Adapted from the deck.gl documentation.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
from django_api.models import Entity, Producer, FoodItem
from django.contrib.auth.models import User

@st.cache_data
def all_users():
    return User.objects.all()

@st.cache_data
def all_entities():
    return Entity.objects.all()

@st.cache_data
def all_producers():
    return Producer.objects.all()

@st.cache_data
def all_food_items():
    return FoodItem.objects.all()

data = []


for entity in all_entities():
    entity_producer = all_producers().filter(entity=entity).first()
    producer_all_food = all_food_items().filter(producer=entity_producer)
    all_food_str = "Currently available foods:"
    for food_item in producer_all_food:
        all_food_str += "\n- " + food_item.name + " (" + str(food_item.quantity) + ")"
    new_data = {
        'name': entity.user.first_name,
        'latitude': float(entity.latitude),
        'longitude': float(entity.longitude),
        'description': entity_producer.description,
        'food_items': all_food_str,
    }

    data.append(new_data)


# Define a layer to display on a map
layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    get_radius=10000,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=["longitude", "latitude"],
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

# Set the viewport location
#view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=10, bearing=0, pitch=0)

# Render
r = pdk.Deck(map_style=None, layers=[layer], tooltip={"text": "{name} \n{food_items}"})

col1, col2 = st.columns([1, 2])

producer_options = []
for producer in all_producers():
    producer_options.append(producer)

with st.sidebar:
    select = st.selectbox("**Select or search for a producer:**", producer_options)
    st.markdown(select.entity.user.first_name)
    with st.expander("See description"):
        st.write(select.description)
    with st.expander("See inventory"):
        producer_all_food = all_food_items().filter(producer=select)
        for food_item in producer_all_food:
            st.write(food_item)


st.pydeck_chart(r)
# st.map(data, use_container_width=False)