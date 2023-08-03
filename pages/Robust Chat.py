import random

import streamlit as st
from google.cloud import firestore
from st_keyup import st_keyup
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
if 'val' not in st.session_state:
    st.session_state.val = ""


messages_collection = db.collection("messages")
st.session_state.chat_messages = []

def route_to_chat_view(word):
    st.session_state.to_chat = word
    st.session_state.num = "2"
    st.button("Return", on_click=route_to_chatlist_view, key=str(random.randint(0, 10000000)))
    st.write(word)

    for document in messages_collection.stream():
        st.session_state.chat_messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                          "content": document.get("msg")})
    for message in st.session_state.chat_messages:
        if (message["fromId"] == this_user and message["toId"] == word) or (message["fromId"] == word and message["toId"] == this_user):
            with st.chat_message(message["role"]):
                st.write(message["fromId"], message["content"])

    def get_prompt(this_user, word):
        st.write("prompt", prompt)
        reload(prompt, this_user, word)

    def dummy(word):
        st.write("prompt", prompt)
        dummy_rel(word)

    def control(this_user, word):
        dummy(word)
        get_prompt(this_user, word)

    prompt = st.text_input('Enter Message', key=str(random.randint(0, 10000000)))
    # st.button('Send', on_click=dummy, args=[word])
    st.button('Send it', on_click=control, args=[this_user, word], key=str(random.randint(0, 10000000)))

def dummy_rel(word):
    route_to_chat_view(word)

def reload(prompt, this_user, word):
    data = {
        'from': this_user,
        'to': word,
        'msg': str(prompt),
        # Add more fields as needed.
    }

    # Use the 'add()' method to add the document to the collection.
    new_document_ref = messages_collection.add(data)
    route_to_chat_view(word)


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

