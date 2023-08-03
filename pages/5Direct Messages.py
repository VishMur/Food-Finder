import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page
from io import BytesIO
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(
    page_title="Direct Messages",
)

def get_image(url_string):
    url = url_string
    r = requests.get(url)
    return BytesIO(r.content)

if st.session_state.log == 0:
    st.header("Access Denied: Please Login First")
    st.subheader("Navigate to the Login tab!")

else:
    this_user = "User1"
    db = firestore.Client.from_service_account_json("firestore-key.json")

    if 'num' not in st.session_state:
        st.session_state.num = "1"
    if 'to_chat' not in st.session_state:
        st.session_state.to_chat = ""

    def route_to_chat_view(word):
        col1, col2, col3, col4 = st.columns(4)

        st.session_state.to_chat = word
        st.session_state.num = "2"
        st.button("Return", on_click=route_to_chatlist_view, key='key_2')

        with col1:
            st.image(get_image(user["profile_img"]), width=100)

        with col2:
            st.header(user["name"])
            st.write(user["user_type"])
        messages_collection = db.collection("messages")
        st.session_state.chat_messages = []

        for document in messages_collection.stream():
            st.session_state.chat_messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                              "content": document.get("msg")})
        for message in st.session_state.chat_messages:
            if (message["fromId"] == this_user and message["toId"] == word) or (message["fromId"] == word and message["toId"] == this_user):
                with st.chat_message(message["role"]):
                    st.write(message["fromId"], message["content"])

    def route_to_chatlist_view():
        st.session_state.to_chat = ""
        st.session_state.num = "1"

    if st.session_state.num == "1":
        st.title("Direct Message Chats")

        users_collection = db.collection("user")
        st.session_state.users = []

        for document in users_collection.stream():
            st.session_state.users.append({"role": "user", "name": document.get("name"),
                                           "profile_img": document.get("profile_img"),
                                           "join_date": document.get("join_date"),
                                           "user_type": document.get("user_type"),})
        for user in st.session_state.users:
            if user["name"] != this_user:
                with st.chat_message(user["role"], avatar="🗞"):
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.image(get_image(user["profile_img"]), width=100)

                    with col2:
                        st.header(user["name"])
                        st.write(user["user_type"])

                    with col3:
                        st.write("")
                    with col4:
                        add_vertical_space(1)
                        st.button("Enter Chat", key=user["name"], on_click=route_to_chat_view, args=[user["name"]])

                        st.write(user["join_date"])





