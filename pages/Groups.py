import streamlit as st
from google.cloud import firestore

st.set_page_config(
    page_title="Groups",
)

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Create a reference to the Google post.
doc_ref = db.collection("farmers").document("T6Mw2vuOJGDg4FcvK7p7")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The name is: ", doc.id)
st.write("The contents are: ", doc.to_dict())



if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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