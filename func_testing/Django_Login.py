import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

import streamlit as st

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
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        ## st.markdown("returned false")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        ## st.markdown("Elif")
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

def verify_password():

    st.session_state["user"] = None
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        st.markdown("create session password_correct")

    def authenticate_user(username_input, password_input):
        st.session_state["user"] = authenticate(
            username=username_input, password=password_input
        )
        st.markdown("Attempted user authentication")
        st.markdown(st.session_state["user"])

        if st.session_state["user"] is None:
            st.markdown("Reached a None user")
            st.session_state["password_correct"] = False
        else:
            st.markdown("Reached an actual user")
            st.session_state["password_correct"] = True
            return True

    if not st.session_state["password_correct"]:
        username_input = st.text_input("Username")
        password_input = st.text_input("Password")
        if(st.button("Login")):
            authenticate_user(username_input, password_input)

    if st.session_state["password_correct"]:
        st.markdown("first True")
        return True

if check_password():
    st.success("You are now logged in!", icon="✅")