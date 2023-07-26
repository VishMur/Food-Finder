import streamlit as st

if 'login' not in st.session_state:
  login_form = st.form(key='login_form')
  username = login_form.text_input(label='username')
  password = login_form.text_input(label='password', type='password')
  submit_button = login_form.form_submit_button(label='submit')


  if submit_button:
    if username in login_details["credentials"]["usernames"]:
        if password == str(login_details["credentials"]["usernames"][username]["password"]):
            st.session_state.username = username
            st.session_state['login'] = True
            st.success("Login successful")
            st.experimental_rerun()
        else:
            st.error("Login failed")

if 'login' in st.session_state:
    st.empty()
    st.write(f"hello, {login_details['credentials']['usernames'][username]['name']}"