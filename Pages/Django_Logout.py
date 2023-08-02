import streamlit as st
from django_api.models import Entity, Producer

st.title("Logout Page")
current_user = st.session_state["user"]
existing_entity = Entity.objects.filter(user=current_user).first()
existing_producer = Producer.objects.filter(entity=existing_entity)

if existing_producer.count():
    st.markdown(existing_producer)

try:
    if st.session_state["password_correct"]:
        logout_message = st.write("You are attempting to log out of your Streamlit account.")
        logout_confirmation = st.error("Are you sure you want to log out?")
        if st.button("Yes, Logout"):
            st.session_state["password_correct"] = False
            st.success("You are now logged out!", icon="✅")

    else:
        st.write("You are not currently logged in.")

except KeyError:
    st.write("You are not currently logged in. Head to our Django Login page to login!")
