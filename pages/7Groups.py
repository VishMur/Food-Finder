import random

import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page
from io import BytesIO
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(
    page_title="Groups",
)

def get_image(url_string):
    url = url_string
    r = requests.get(url)
    return BytesIO(r.content)

if st.session_state.log == 0:
    st.header("Access Denied: Please Login First")
    st.subheader("Navigate to the Login tab!")

else:
    this_user = "TestUser"
    db = firestore.Client.from_service_account_json("firestore-key.json")

    if 'num' not in st.session_state:
        st.session_state.num = 1
    if 'to_chat' not in st.session_state:
        st.session_state.to_chat = ""
    if 'title' not in st.session_state:
        st.session_state.title = 0
    # if 'paschat' not in st.session_state:
    #     st.session_state.paschat = ""

    def route_to_chat_view(word):

        st.session_state.to_chat = word
        st.session_state.num = 2
        col11, col12, col13, col14 = st.columns(4)

        with col11:
            try:
                st.session_state.title += 1
                if st.session_state.title < 2:
                    st.title("Group Chat")
                else:
                    route_to_chatlist_view()
            except:
                pass
        with col12:
            st.write("")
        with col13:
            st.write("")
        with col14:
            add_vertical_space(2)
            st.button("Go Back to Chat List", on_click=route_to_chatlist_view, key="key_16")

        messages_collection = db.collection("messages")
        st.session_state.chat_messages = []

        for document in messages_collection.stream():
            st.session_state.chat_messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"),
                                              "content": document.get("msg")})
        st.session_state.chat_messages.reverse()
        for message in st.session_state.chat_messages:
            col1, col2 = st.columns(2)
            get_img1 = ""
            get_img2 = ""
            for user in st.session_state.users:
                if user["name"] == word:
                    get_img1 = user["profile_img"]
                elif user["name"] == this_user:
                    get_img2 = user["profile_img"]


            if (message["fromId"] == this_user and message["toId"] == word) or (message["fromId"] == word and message["toId"] == this_user):
                if message["fromId"] != this_user:
                    with col1:
                        with st.chat_message(message["role"], avatar="📄"):
                            col3, col4, col5, col6, col7 = st.columns(5)
                            with col3:
                                st.image(get_image(get_img1), width=40)
                            with col4:
                                st.subheader(message["fromId"])
                            with col5:
                                st.write("")
                            with col6:
                                st.write("")
                            with col7:
                                st.write("")
                            st.write(message["content"])
                else:
                    with col2:
                        with st.chat_message(message["role"], avatar="📄"):
                            col3, col4, col5, col6, col7 = st.columns(5)
                            with col3:
                                st.image(get_image(get_img2), width=40)
                            with col4:
                                st.subheader(message["fromId"])
                            with col5:
                                st.write("")
                            with col6:
                                st.write("")
                            with col7:
                                st.write("")
                            st.write(message["content"])

    def route_to_chatlist_view():
        st.session_state.to_chat = ""
        st.session_state.num = 1
        st.session_state.title = 0

    if st.session_state.num == 1:
        st.title("Groups")

        gc_collection = db.collection("group_chats")
        st.session_state.grchats = []

        for document in gc_collection.stream():
            st.session_state.grchats.append({"role": "user",
                                             "gc_name": document.get("group_name"),
                                           "group_img": document.get("group_img"),
                                           "names": document.get("names"),
                                           "date": document.get("creation_date"),})
        for chat in st.session_state.grchats:
            if  this_user in chat["names"]:
                with st.chat_message(chat["role"], avatar="🗞"):
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.image(get_image(chat["group_img"]), width=140)

                    with col2:
                        st.subheader(chat["gc_name"])
                        st.write(chat["names"])

                    with col3:
                        st.write("")

                    with col4:
                        add_vertical_space(1)
                        st.button("Enter Chat", key=chat["gc_name"], on_click=route_to_chat_view, args=[chat["gc_name"]])
                        add_vertical_space(2)
                        st.write(chat["date"])
    elif st.session_state.num == 2:
        try:
            route_to_chat_view(st.session_state.to_chat)
        except:
            pass




