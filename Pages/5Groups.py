import streamlit as st
from google.cloud import firestore

st.set_page_config(
    page_title="Groups",
)

if st.session_state.log == 0:
    st.header("Access Denied: Please Login First")
    st.subheader("Navigate to the Login tab!")

else:
    db = firestore.Client.from_service_account_json("firestore-key.json")

    messages_collection = db.collection("messages")
    st.session_state.messages = []

    # get all messages
    for document in messages_collection.stream():
        st.write("Document: ", document.id)
        st.write("Contents: ", document.to_dict())
        st.session_state.messages.append({"role": "user", "fromId": document.get("from"), "toId": document.get("to"), "content": document.get("msg")})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["fromId"] + " ----- " + message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     for response in openai.ChatCompletion.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream=True,
    #     ):
    #         full_response += response.choices[0].delta.get("content", "")
    #         message_placeholder.markdown(full_response + "▌")
    #     message_placeholder.markdown(full_response)
    # st.session_state.messages.append({"role": "assistant", "content": full_response})