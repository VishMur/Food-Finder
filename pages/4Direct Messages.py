import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Direct Messages",
)

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
        st.session_state.to_chat = word
        st.session_state.num = "2"
        st.button("Return", on_click=route_to_chatlist_view, key='key_2')
        st.write(word)

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

