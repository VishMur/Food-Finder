import streamlit as st
from google.cloud import firestore

st.set_page_config(
    page_title="Groups",
)

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Create a reference to the Google post.
doc_ref = db.collection("farmers").document("T6Mw2vuOJGDg4FcvK7p7")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The name is: ", doc.id)
st.write("The contents are: ", doc.to_dict())