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
                    st.title("Chat")
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

        gc_messages_collection = db.collection("group_chats")
        st.session_state.gc_chat_messages = []

        with st.spinner("Loading Chats..."):
            for i in range(1000):
                st.session_state.gc_chat_messages.append("")

            for doc in gc_messages_collection.stream():
                for subdoc in doc.reference.collection("messages").stream():
                    st.session_state.gc_chat_messages[subdoc.get("id") - 1] = (
                                                             {"role": "user",
                                                              "name": subdoc.get("sender"),
                                                              "content": subdoc.get("msg"),
                                                              "ord": subdoc.get("id")})

            for message in st.session_state.gc_chat_messages:
                if message != "":
                    col1, col2 = st.columns(2)
                    if message["name"] != this_user:
                        with col1:
                            with st.chat_message(message["role"], avatar="📄"):
                                col3, col4, col5, col6, col7 = st.columns(5)
                                with col3:
                                    st.subheader(message["name"])
                                with col4:
                                    st.write("")
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
                                    st.subheader(message["name"])
                                with col4:
                                    st.write("")
                                with col5:
                                    st.write("")
                                with col6:
                                    st.write("")
                                with col7:
                                    st.write("")
                                st.write(message["content"])
                try:
                    st.chat_input(placeholder="Demo account \"TestUser\" restricts sending messages.", disabled=True, key=random.randrange(100000))
                except:
                    pass

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




