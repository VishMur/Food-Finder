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
        user = authenticate(
            username=st.session_state["username"], password=st.session_state["password"]
        )

        if user is not None:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.success("You are now logged in!", icon="✅")