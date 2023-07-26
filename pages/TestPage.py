import streamlit as st
#
# import streamlit as st
#
# st.session_state['login'] = False
#
# if st.session_state['login'] == False:
#     st.write("login")
#     if st.button("login"):
#         st.session_state['login'] == True
#         st.empty()
#
#
# if st.session_state['login'] == True:
#     st.write("logout")
#     if st.button("log out"):
#         st.session_state['login'] == False
#         st.empty()

import streamlit as st

##  Logic control
def c(): st.session_state.b1 = True
def d(): st.session_state.b1 = False
if 'b1' not in st.session_state: st.session_state.b1 = False

## Think of the placeholder here as a list initialized with no elements
ph = st.empty()

## Here you start adding elements to the placeholder
with ph.container():
    st.write("1️⃣ First element in placeholder")                      # ph[0] = a st.write
    st.button("1️⃣ Second element in ph (Go to page 2)",on_click=c)   # ph[1] = a st.button

if st.session_state.b1:
    with ph.container():
        st.write("2️⃣ This overwrites the first element")    # ph[0] = a new st.write
        st.write("2️⃣ This overwrites the second element")   # ph[1] = a new st.write
        st.write("2️⃣ Third element in placeholder")         # ph[2] = a st.write
        st.button("2️⃣ Fourth element in ph (Go to page 3)",on_click=d)     # ph[3] = a st.button
