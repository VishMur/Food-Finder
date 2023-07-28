import random

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
if 'inputted_text' not in st.session_state:
    st.session_state.refresh = "0"
if 'to_chat' not in st.session_state:
    st.session_state.to_chat = ""

messages_collection = db.collection("messages")
st.session_state.chat_messages = []

def route_to_chat_view(word):
    rand_key = random.randint(0, 10000000)
    st.session_state.to_chat = word
    st.button("Return", on_click=route_to_chatlist_view, key=str(rand_key))
    st.write(word)

    for document in messages_collection.stream():
        st.session_state.chat_messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                          "content": document.get("msg")})
    for message in st.session_state.chat_messages:
        if (message["fromId"] == this_user and message["toId"] == word) or (message["fromId"] == word and message["toId"] == this_user):
            with st.chat_message(message["role"]):
                st.write(message["fromId"], message["content"])

    st.button("Return", on_click=reload, key="1232222")

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

def reload():
    st.write("reloaded")
    route_to_chat_view("User2")


def route_to_chatlist_view():
    st.session_state.to_chat = ""
    st.session_state.num = "1"

if st.session_state.num == "1":
    st.title("Chats")

    messages_collection = db.collection("messages")
    st.session_state.messages = []

    for document in messages_collection.stream():
        st.session_state.messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                          "content": document.get("msg")})
    for message in st.session_state.messages:
        if message["fromId"] != this_user:
            with st.chat_message(message["role"]):
                st.button(message["fromId"], key=message["fromId"], on_click=route_to_chat_view, args=[message["fromId"]])

elif st.session_state.refresh == "1":
    st.write("wow")