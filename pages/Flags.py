import streamlit as st
from google.cloud import firestore

if 'num' not in st.session_state:
    st.session_state.num = "1"

this_user = "User1"
db = firestore.Client.from_service_account_json("firestore-key.json")

def update2():
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
                st.button(message["fromId"], key=message["fromId"])

    st.session_state.num = "2"

def update3():
    st.session_state.num = "1"

# st.write(st.session_state.num)
if st.session_state.num == "1":
    st.button("Perform calculation 2", on_click=update2, key='key_2')
else:
    st.button("Perform calculation 3", on_click=update3, key='key_3')
