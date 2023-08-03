import streamlit as st

if st.session_state.log == 0:
    st.header("Access Denied: Please Login First")
    st.subheader("Navigate to the Login tab!")

else:
    st.write("This is my profile")