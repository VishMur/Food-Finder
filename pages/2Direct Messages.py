import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Direct Messages",
)

this_user = "User1"
db = firestore.Client.from_service_account_json("firestore-key.json")

if 'num' not in st.session_state:
    st.session_state.num = "1"
if 'to_chat' not in st.session_state:
    st.session_state.to_chat = ""

def update2(word):
    st.session_state.to_chat = word
    messages_collection = db.collection("messages")
    st.session_state.chat_messages = []
    for document in messages_collection.stream():
        st.session_state.chat_messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                          "content": document.get("msg")})
    for message in st.session_state.chat_messages:
        if (message["fromId"] == this_user and message["toId"] == word) or (message["fromId"] == word and message["toId"] == this_user):
            with st.chat_message(message["role"]):
                st.write(message["fromId"], message["content"])

    st.session_state.num = "2"
    st.button("Return", on_click=update3, key='key_2')

def update3():
    st.session_state.to_chat = ""
    st.session_state.num = "1"

st.write(st.session_state.to_chat)
if st.session_state.num == "1":
    messages_collection = db.collection("messages")
    st.session_state.messages = []

    for document in messages_collection.stream():
        st.write("Document: ", document.id)
        st.write("Contents: ", document.to_dict())
        st.session_state.messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                          "content": document.get("msg")})

    for message in st.session_state.messages:
        if message["fromId"] != this_user:
            with st.chat_message(message["role"]):
                st.button(message["fromId"], key=message["fromId"], on_click=update2, args=[message["fromId"]])

