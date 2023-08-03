import streamlit as st
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


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

        return user

form = CustomUserCreationForm()

if st.button("Register"):
    if (form.username_clean()
            and form.name_clean()
            and form.email_clean()
            and form.clean_password2()
        ):
        form.save()
        st.success("Account successfully created! You can now login with your new credentials!", icon="✅")
