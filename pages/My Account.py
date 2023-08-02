import streamlit as st
from django_api.models import Entity, Producer
from pages.Django_Login import check_password

# if user is logged in:
    # check if user has a producer account linked:
        # display if so
        # display register for a producer account if not
    # check if user has a volunteer account linked:
        # display if so
        # display register for a volunteer account if not
        ## optional: have a saved/bookmarked locations?
# else (not logged in):
    # prompt check_password

# on the scatter2 map,
    ## optional: registered volunteers can bookmark
    # if producer, highlight the locations that are registered as yours

st.title("My Account")




def get_user_entity():
    current_user = st.session_state["user"]
    entity = Entity.objects.all().filter(user=current_user).first()
    return entity

def post_to_db():
    st.spinner("posting to db")


# first login is a user
if check_password():
    current_user = st.session_state["user"]

    left_column, right_column = st.columns(2)
    with left_column:
        st.text_input(label="**First name or Organization name***", value=current_user.first_name)

    with right_column:
        st.text_input(label="Last name", value=current_user.last_name)

    with st.container():
        st.text_input(label="Email address", value=current_user.email)

    with st.container():
        st.header("Additional Info")
        if (get_user_entity()):
            st.text_input(label="Phone number", value=get_user_entity().phone_number)
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(label="**Latitude***", value=get_user_entity().latitude)
            with col2:
                st.text_input(label="**Longitude***", value=get_user_entity().longitude)
            st.text_input(label="Address", value=get_user_entity().address)
        else:
            st.text_input(label="Phone number")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(label="**Latitude***")
            with col2:
                st.text_input(label="**Longitude***")
            st.text_input(label="Address")

    st.button("Save changes", on_click=post_to_db())


else:
    st.markdown("You are not currently logged in. Log in?")


