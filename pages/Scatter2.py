"""
ScatterplotLayer
================

Plot of the number of exits for various subway stops within San Francisco, California.

Adapted from the deck.gl documentation.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import os

from django.core.wsgi import get_wsgi_application
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

from django_api.models import Entity, Producer, FoodItem, Volunteer, ProducerBookmark
from django.contrib.auth.models import User



import streamlit as st

@st.cache_data
def all_users():
    return User.objects.all()

@st.cache_data
def all_entities():
    return Entity.objects.all()

@st.cache_data
def all_volunteers():
    return Volunteer.objects.all()

@st.cache_data
def all_producers():
    return Producer.objects.all()

@st.cache_data
def all_food_items():
    return FoodItem.objects.all()

def bookmark_button_disabled():
    user = st.session_state["user"]
    user_entity = all_entities().filter(user=user).first()
    volunteer = all_volunteers().filter(entity=user_entity).first()
    st.session_state["volunteer"] = volunteer
    if volunteer is None:
        return True
    else:
        return False


def bookmark_help_message():
    if bookmark_button_disabled():
        return "Login or create a volunteer account to bookmark locations!"
    else:
        return "Bookmark locations for the future!"



data = []


for producer in all_producers():
    entity = producer.entity
    producer_all_food = all_food_items().filter(producer=producer)
    all_food_str = "Currently available foods:"

    for food_item in producer_all_food:
        all_food_str += "\n- " + food_item.name + " (" + str(food_item.quantity) + ")"

    if producer_all_food.count() == 0:
        all_food_str += "\n None ATM. Check back later!"


    new_data = {
        'name': entity.user.first_name,
        'latitude': float(entity.latitude),
        'longitude': float(entity.longitude),
        'description': producer.description,
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

# Render


col1, col2 = st.columns([1, 2])

producer_options = []
for producer in all_producers():
    producer_options.append(producer)

with st.sidebar:
    select = st.selectbox("**Select or search for a producer:**", producer_options)
    st.subheader(select.entity.user.first_name)
    st.write(f"Deliveries: {select.deliveries}")
    st.write(f":pushpin: {select.entity.address}")
    st.write(f":earth_americas: {select.website_link}")
    st.write(f":telephone_receiver: {select.entity.phone_number}")
    st.caption(f":round_pushpin: {select.entity.latitude}, {select.entity.longitude}")
    with st.expander("See description"):
        st.write(select.description)
    with st.expander("See inventory"):
        producer_all_food = all_food_items().filter(producer=select)
        for food_item in producer_all_food:
            st.markdown(f"{food_item.name} ({food_item.quantity})")


    if(st.button("Bookmark producer",
                 disabled=bookmark_button_disabled(),
                 help=bookmark_help_message())
    ):
        try:
            new_bookmark = ProducerBookmark.objects.create(
                producer=select,
                volunteer=st.session_state.volunteer,
            )
            new_bookmark.save()
            st.toast("Producer successfully bookmarked!", icon="✅")
        except IntegrityError:
            st.error("Producer already bookmarked!")


view_state = pdk.ViewState(latitude=float(select.entity.latitude), longitude=float(select.entity.longitude), zoom=3, bearing=0, pitch=0)

r = pdk.Deck(map_style=None, initial_view_state=view_state, layers=[layer], tooltip={"text": "{name} \n{food_items}"})
st.pydeck_chart(r)
# st.map(data, use_container_width=False)