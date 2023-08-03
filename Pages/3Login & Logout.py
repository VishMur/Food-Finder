import streamlit as st
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

import streamlit as st
from django_api.models import Entity, Producer
import streamlit as st

if st.session_state.log == 0:
    # Create an empty container
    placeholder = st.empty()

    actual_email = "test@gmail.com"
    actual_password = "test"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email", key="username")
        password = st.text_input("Password", type="password", key="password")
        submit = st.form_submit_button("Login")



    def check_password():

        """Returns `True` if the user had a correct password."""

        # Error occurs on login page, then src code is changed, then cache is cleared, NO refresh,
        # and attempt to re-login
        # occurs w/o password being entered (on_change)
        # occurs infinite times in current session

        def password_entered():
            """Checks whether a password entered by the user is correct."""

            ## st.markdown('password entered')

            user = None

            ## st.write("text input was changed")
            if ((st.session_state["username"] != "") and
                    (st.session_state["password"] != "")):
                ## st.markdown(st.session_state.username)
                ## st.markdown(st.session_state.password)
                user = authenticate(
                    username=st.session_state["username"], password=st.session_state["password"]
                )

                ## st.write("attempted authentication")

            st.session_state["user"] = user

            ## st.write(user)

            if user is not None:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store username + password
                del st.session_state["username"]
                ## st.markdown("session pass = True")
            else:
                st.session_state["password_correct"] = False
                ## st.markdown("session pass = False")

        if "password_correct" not in st.session_state:
            ## st.markdown("st session state no pass_corr")
            # First run, show inputs for username + password.
            if submit:
                password_entered()
            ## st.markdown("returned false")
            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            ## st.markdown("Elif")
            if submit:
                password_entered()
                st.error("😕 User not known or password incorrect")
            return False
        else:
            # Password correct.
            st.session_state.log = 1
            return True


    if check_password():
        pass

    if check_password():
        st.success("You are now logged in!", icon="✅")

    # if submit and email == actual_email and password == actual_password:
    #     # If the form is submitted and the email and password are correct,
    #     # clear the form/container and display a success message
    #     placeholder.empty()
    #     st.session_state.log = 1
    #     st.success("Login successful")
    # elif submit and email != actual_email and password != actual_password:
    #     st.error("Login failed")
    # else:
    #     pass

elif st.session_state.log == 1:
    current_user = st.session_state["user"]
    existing_entity = Entity.objects.filter(user=current_user).first()
    existing_producer = Producer.objects.filter(entity=existing_entity)

    try:
        if st.session_state["password_correct"]:
            logout_message = st.write("You are attempting to log out of your Streamlit account.")
            logout_confirmation = st.error("Are you sure you want to log out?")
            if st.button("Yes, Logout"):
                st.session_state["password_correct"] = False
                st.session_state.log = 0
                st.experimental_rerun()

        else:
            st.write("You are not currently logged in.")

    except KeyError:
        st.write("You are not currently logged in. Head to our Django Login page to login!")
