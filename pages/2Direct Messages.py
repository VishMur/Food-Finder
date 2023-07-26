import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Direct Messages",
)

db = firestore.Client.from_service_account_json("firestore-key.json")

if st.button('Switch Pages'):
    st.write("YOOOO")
    switch_page("groups")