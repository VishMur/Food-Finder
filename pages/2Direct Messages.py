import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page

this_user = "User1"

st.set_page_config(
    page_title="Direct Messages",
)

db = firestore.Client.from_service_account_json("firestore-key.json")

# if st.button('Switch Pages'):
#     st.write("YOOOO")
#     switch_page("groups")

messages_collection = db.collection("messages")
st.session_state.messages = []

for document in messages_collection.stream():
    st.write("Document: ", document.id)
    st.write("Contents: ", document.to_dict())
    st.session_state.messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"), "content": document.get("msg")})

for message in st.session_state.messages:
    if message["fromId"] != this_user:
        with st.chat_message(message["role"]):
                st.button(message["fromId"], key=message["fromId"])

if st.session_state.get('User2'):
    st.write("caught")
