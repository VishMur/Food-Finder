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


# first login is a user
if check_password():
    current_user = st.session_state["user"]
    current_entity = get_user_entity()

    left_column, right_column = st.columns(2)
    with left_column:
        first_name_input = st.text_input(label="**First name or Organization name***", value=current_user.first_name)

    with right_column:
        last_name_input = st.text_input(label="Last name", value=current_user.last_name)

    with st.container():
        email_input = st.text_input(label="Email address", value=current_user.email)

    with st.container():
        st.subheader("Additional Info")
        if (get_user_entity()):
            phone_number_input = st.text_input(label="Phone number", value=get_user_entity().phone_number)
            col1, col2 = st.columns(2)
            with col1:
                latitude_input = st.text_input(label="**Latitude***", value=get_user_entity().latitude)
            with col2:
                longitude_input = st.text_input(label="**Longitude***", value=get_user_entity().longitude)
            address_input = st.text_input(label="Address", value=get_user_entity().address)
        else:
            phone_number_input = st.text_input(label="Phone number")
            col1, col2 = st.columns(2)
            with col1:
                latitude_input = st.text_input(label="**Latitude***")
            with col2:
                longitude_input = st.text_input(label="**Longitude***")
            address_input = st.text_input(label="Address")


    def name_clean():
        if first_name_input == "":
            st.warning('First name or Organization name is required!', icon="⚠️")
            return False
        else:
            return True

    def latitude_clean():
        if latitude_input == "":
            st.warning('Latitude is required!', icon="⚠️")
            return False
        # some other verification that latitude are within bounds
        try:
            float(latitude_input)
            return True
        except ValueError:
            st.warning('Latitude must be a valid decimal!', icon="⚠️")
            return False

    def longitude_clean():
        if longitude_input == "":
            st.warning('Longitude is required!', icon="⚠️")
            return False
        # some other verification that longitude are within bounds
        try:
            float(latitude_input)
            return True
        except ValueError:
            st.warning('Longitude must be a valid decimal!', icon="⚠️")
            return False


    def post_to_db(entity):
        current_user.first_name = first_name_input
        current_user.last_name = last_name_input
        current_user.email = email_input

        current_user.save()

        if entity is None:
            if latitude_input != "" and longitude_input != "":
                new_entity = Entity.objects.create(user=current_user,
                                                   phone_number=phone_number_input,
                                                   latitude=latitude_input,
                                                   longitude=longitude_input,
                                                   address=address_input)
                new_entity.save()
        else:
            current_entity.phone_number = phone_number_input
            current_entity.latitude = latitude_input
            current_entity.longitude = longitude_input
            current_entity.address = address_input
            current_entity.save()

    if st.button("Save changes"):
        if (name_clean()
            and latitude_clean()
            and longitude_clean()
        ):
            post_to_db(current_entity)
            st.success("Account successfully updated!", icon="✅")



else:
    st.markdown("You are not currently logged in. Log in?")


