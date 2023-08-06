import streamlit as st
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate
from streamlit_extras.add_vertical_space import add_vertical_space

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

import streamlit as st
from django_api.models import Entity, Producer
import streamlit as st
import streamlit as st
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

if st.session_state.log == 0:
    # Create an empty container
    st.write("For demonstration purposes use login \"ucacopperview\" and password \"testing321\" to log into "
             "the \"TestUser\" account.")
    placeholder = st.empty()

    actual_email = "test@gmail.com"
    actual_password = "test"

    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Username", key="username")
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

    add_vertical_space(1)
    st.markdown("<h4 style='text-align: center; color: black;'>or", unsafe_allow_html=True)
    add_vertical_space(1)

    placeholder2 = st.empty()

    # Insert a form in the container
    with placeholder2.form("register"):
        st.markdown("#### Register here")
        class CustomUserCreationForm(UserCreationForm):

            username = st.text_input("**Username***")
            # username = forms.CharField(label='username', min_length=5, max_length=150)
            name = st.text_input("**First Name or Organization Name***")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            # email = forms.EmailField(label='email')
            password = st.text_input("**Password***", type='password')
            confirm_password = st.text_input("**Confirm Password***", type='password')

            # password1 = forms.CharField(label='password', widget=forms.PasswordInput)
            # password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

            def username_clean(self):
                if not self.username:
                    st.warning('Username is required!', icon="⚠️")
                    return False

                duplicate_username = User.objects.filter(username=self.username)
                if duplicate_username.count():
                    st.warning('Username already taken!', icon="⚠️")
                    return False
                else:
                    return True

            def name_clean(self):
                if not self.name:
                    st.warning('Name is required!', icon="⚠️")
                    return False
                else:
                    return True

            def email_clean(self):

                if self.email != "":
                    try:
                        validate_email(self.email)
                    except ValidationError:
                        st.warning('Not a valid email!', icon="⚠️")
                        return False

                    duplicate_email = User.objects.filter(email=self.email)
                    if duplicate_email.count():
                        st.warning('Email already taken!', icon="⚠️")
                        return False

                return True

            def clean_password2(self):
                password1 = self.password
                password2 = self.confirm_password

                try:
                    validate_password(password1)
                except ValidationError:
                    st.warning("""
                    - Your password can't be too similar to your other information. 
                    - Your password must contain at least 8 characters.
                    - Your password can't be a commonly used password.
                    - Your password can't be entirely numeric.""", icon="⚠️")
                    return False

                if password1 == "" or password2 == "":
                    st.warning("Passwords can't be blank!", icon="⚠️")
                    return False
                elif password1 != password2:
                    st.warning("Passwords don't match!", icon="⚠️")
                    return False
                else:
                    return True

            def save(self, commit=True):
                user = User.objects.create_user(
                    username=self.username,
                    email=self.email,
                    password=self.password,
                )

                user.first_name = self.name
                user.last_name = self.last_name

                user.save()

                return user


        form = CustomUserCreationForm()

        if st.form_submit_button("Register"):
            if (form.username_clean()
                    and form.name_clean()
                    and form.email_clean()
                    and form.clean_password2()
            ):
                form.save()
                st.success("Account successfully created! You can now login with your new credentials!", icon="✅")



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
