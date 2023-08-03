"""
GeoJsonLayer
===========

Property values in Vancouver, Canada, adapted from the deck.gl example pages.
"""


import math

import pandas as pd
import pydeck as pdk
import streamlit as st
import pygris
from streamlit_folium import st_folium


# Load in the JSON data
DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
# json = pd.read_json(DATA_URL)
json = pygris.tracts(state="UT", county="Utah")

df = pd.DataFrame()


# Parse the geometry out in Pandas
df["coordinates"] = json.values[:,12]

df1 = json.explore()

view_state = pdk.ViewState(
    **{"latitude": 49.254, "longitude": -123.13, "zoom": 11, "maxZoom": 16, "pitch": 45, "bearing": 0}
)


polygon_layer = pdk.Layer(
    "PolygonLayer",
    df1,
    id="geojson",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
)

r = pdk.Deck(
    polygon_layer,
    initial_view_state=view_state,
    map_style=pdk.map_styles.LIGHT,
)
# st.pydeck_chart(r)

@st.cache_resource
def load_data():
    capitol_tracts = pygris.tracts(state = "TX", cb = True,
                            subset_by = {"1100 Congress Ave., Austin, TX 78701": 500000})
    data = []
    data.append(capitol_tracts.explore())

    return data

st_data = st_folium(load_data()[0], width=725)