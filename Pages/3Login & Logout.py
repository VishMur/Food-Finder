import streamlit as st

if st.session_state.log == 0:
    # Create an empty container
    placeholder = st.empty()

    actual_email = "test@gmail.com"
    actual_password = "test"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and email == actual_email and password == actual_password:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.session_state.log = 1
        st.success("Login successful")
    elif submit and email != actual_email and password != actual_password:
        st.error("Login failed")
    else:
        pass

elif st.session_state.log == 1:
    logout_button = st.button("Logout")
    if logout_button:
        st.session_state.log = 0
        st.success("Logout successful")