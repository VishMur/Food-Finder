from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form

import streamlit as st


class CustomUserCreationForm(UserCreationForm):

    username = st.text_input("**Username***")
    # username = forms.CharField(label='username', min_length=5, max_length=150)
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

    def email_clean(self):

        if self.email != "":
            duplicate_email = User.objects.filter(email=CustomUserCreationForm.email)
            if duplicate_email.count():
                st.warning('Email already taken!', icon="⚠️")
                return False
        else:
            return True

    def clean_password2(self):
        password1 = self.password
        password2 = self.confirm_password

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
            self.username,
            self.email,
            self.password,
        )
        return user

form = CustomUserCreationForm()

if st.button("Register"):
    if (form.username_clean() and form.email_clean() and form.clean_password2()):
        print("valid form!")
        form.save()
    else:
        print('invalid form!')