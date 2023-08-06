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

from streamlit_extras.add_vertical_space import add_vertical_space


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

RED_ICON_URL = "https://cdn1.iconfinder.com/data/icons/color-bold-style/21/14_2-512.png"
BLUE_ICON_URL = "https://cdn3.iconfinder.com/data/icons/flat-pro-basic-set-1-1/32/location-blue-512.png"

red_icon_data = {
    "url": RED_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,

}

blue_icon_data = {
    "url": BLUE_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,

}

producer_data = []
volunteer_data = []


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
        'red_icon_data': red_icon_data,
    }

    producer_data.append(new_data)

for volunteer in all_volunteers():
    new_data = {
        'name':volunteer.entity.user.first_name,
        'latitude': float(volunteer.entity.latitude),
        'longitude': float(volunteer.entity.longitude),
        'food_items': volunteer.entity.user.email,
        'deliveries': volunteer.deliveries,
        'blue_icon_data': blue_icon_data,
    }

    volunteer_data.append(new_data)

# Define a layer to display on a map
producer_data_layer = pdk.Layer(
    type="IconLayer",
    data=producer_data,
    get_icon="red_icon_data",
    get_size=3,
    size_scale=15,
    get_position=["longitude", "latitude"],
    pickable=True,
)


volunteer_data_layer = pdk.Layer(
    type="IconLayer",
    data=volunteer_data,
    get_icon="blue_icon_data",
    get_size=3,
    size_scale=15,
    get_position=["longitude", "latitude"],
    pickable=True,
)

# Set the viewport location

# Render

st.header("Interactive Map")
st.write("""
        Our goal: allow consumers within food deserts to access **nutritious, affordable food**.
        
        \nThus, we have compiled data on **local food producers**, such as food pantries and banks, along with
        information on **nearby volunteers** in order to **empower a community** to tackle the problems of 
        food waste and food deserts.""")

st.write("---")







producer_options = []
for producer in all_producers():
    producer_options.append(producer)


def display_producer(producer):
    global producer_all_food, food_item
    st.subheader(f"{bookmarked()} {producer.entity.user.first_name}")
    st.write(f"Deliveries: {producer.deliveries}")
    st.write(f":pushpin: {producer.entity.address}")
    st.write(f":earth_americas: {producer.website_link}")
    st.write(f":telephone_receiver: {producer.entity.phone_number}")
    st.caption(f":round_pushpin: {producer.entity.latitude}, {producer.entity.longitude}")
    with st.expander("See description"):
        st.write(producer.description)
    with st.expander("See inventory"):
        producer_all_food = all_food_items().filter(producer=producer)
        for food_item in producer_all_food:
            st.markdown(f"{food_item.name} ({food_item.quantity})")


with st.sidebar:
    select = st.selectbox("**Select or search for a producer:**", producer_options)

    try:
        user_entity = all_entities().filter(user=st.session_state.user).first()
    except (AttributeError, KeyError) as e:
        first_user = User.objects.all().first()
        user_entity = all_entities().filter(user=first_user).first()
    volunteer = all_volunteers().filter(entity=user_entity).first()

    bookmark = ProducerBookmark.objects.all().filter(producer=select, volunteer=volunteer).first()

    def bookmarked():
        if bookmark is None:
            return ""
        else:
            return ":bookmark:"


    display_producer(select)

    bookmark_left, bookmark_right = st.columns(2)

    if 'user' in st.session_state:

        with bookmark_left:
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
                    st.experimental_rerun()
                except IntegrityError:
                    st.error("Producer already bookmarked!")
        with bookmark_right:
            if(st.button("Remove bookmark", key="searchbar_remove_button")):
                if bookmark is not None:
                    bookmark.delete()
                    st.toast("Bookmark successfully removed!", icon="✅")
                    st.experimental_rerun()

    st.divider()

    if 'volunteer' in st.session_state:
        st.subheader("View bookmarks")
        add_vertical_space()
        volunteer_bookmarks = ProducerBookmark.objects.all().filter(volunteer=volunteer)
        if volunteer_bookmarks.count() == 0:
            st.write("You have no bookmarks!")
        count = 0
        for bookmark in volunteer_bookmarks:
            display_producer(bookmark.producer)
            if st.button("Remove bookmark", key="remove_bookmark"+str(count)):
                bookmark.delete()
                st.toast("Bookmark successfully removed!", icon="✅")
                st.experimental_rerun()
            st.divider()
            count += 1


view_state = pdk.ViewState(latitude=float(select.entity.latitude), longitude=float(select.entity.longitude), zoom=10, bearing=0, pitch=0)


producer_all_food = all_food_items().filter(producer=select)
select_food_str = "Currently available foods:"

for food_item in producer_all_food:
    select_food_str += "\n- " + food_item.name + " (" + str(food_item.quantity) + ")"

if producer_all_food.count() == 0:
    select_food_str += "\n None ATM. Check back later!"

selected_data = []
select_data = {
    'name': select.entity.user.first_name,
    'latitude': float(select.entity.latitude),
    'longitude': float(select.entity.longitude),
    'description': select.description,
    'food_items': select_food_str,
}
selected_data.append(select_data)

selected_data_layer = pdk.Layer(
    "ScatterplotLayer",
    data=selected_data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius=1000,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=1000,
    line_width_min_pixels=1,
    get_position=["longitude", "latitude"],
    get_fill_color=[255, 140, 0],
)

layers = [selected_data_layer, producer_data_layer, volunteer_data_layer]
r = pdk.Deck(map_style=None, initial_view_state=view_state, layers=layers, tooltip={"text": "{name} \n{food_items}"})
st.pydeck_chart(r)

st.write("**Welcome to our interactive map.**")
st.markdown(""":point_up: Our map displays **location and other basic info** on nearby food producers
          and volunteers.""")

with st.container():
    col1, col2 = st.columns([1,10])
    with col1:
        st.image(RED_ICON_URL, width=50)
    with col2:
        st.write("Our red icon displays locations of local producers.")
with st.container():
    col1, col2 = st.columns([1,10])
    with col1:
        st.image(BLUE_ICON_URL, width=50)
    with col2:
        st.write("Our blue icon displays the location of nearby volunteers.")

st.markdown(""":point_left: On the left is a **sidebar** that enables you to search for a specific
         organization, location, or person, and provides you with additional
         information.""")

# st.map(volunteer_data, use_container_width=False)