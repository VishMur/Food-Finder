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

ICON_URL = "https://cdn1.iconfinder.com/data/icons/color-bold-style/21/14_2-512.png"

icon_data = {
    "url": ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,

}

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
        'icon_data': icon_data,
    }

    data.append(new_data)


# Define a layer to display on a map
layer = pdk.Layer(
    type="IconLayer",
    data=data,
    get_icon="icon_data",
    get_size=3,
    size_scale=15,
    get_position=["longitude", "latitude"],
    pickable=True,
)

# Set the viewport location

# Render


col1, col2 = st.columns([1, 2])

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

    user_entity = all_entities().filter(user=st.session_state.user).first()
    volunteer = all_volunteers().filter(entity=user_entity).first()

    bookmark = ProducerBookmark.objects.all().filter(producer=select, volunteer=volunteer).first()

    def bookmarked():
        if bookmark is None:
            return ""
        else:
            return ":bookmark:"


    display_producer(select)

    bookmark_left, bookmark_right = st.columns(2)

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

    if st.session_state.volunteer is not None:
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

r = pdk.Deck(map_style=None, initial_view_state=view_state, layers=[layer], tooltip={"text": "{name} \n{food_items}"})
st.pydeck_chart(r)
# st.map(data, use_container_width=False)