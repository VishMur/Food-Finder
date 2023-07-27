import streamlit as st

dark = '''
<style>
    .stApp {
    background-color: black;
    }
</style>
'''

light = '''
<style>
    .stApp {
    background-color: white;
    }
</style>
'''

st.markdown(light, unsafe_allow_html=True)

# Create a toggle button
toggle = st.button("Toggle theme")

# Use a global variable to store the current theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Change the theme based on the button state
if toggle:
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# Apply the theme to the app
if st.session_state.theme == "dark":
    st.markdown(dark, unsafe_allow_html=True)
else:
    st.markdown(light, unsafe_allow_html=True)

# Display some text
st.write("This is a streamlit app with a toggle button for themes.")