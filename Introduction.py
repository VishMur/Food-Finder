import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Food Finder")
st.write("A GNEC Hackathon Submission")

# st.sidebar.success("Select a demo above.")
#     **👈 Select a demo from the sidebar** to see some examples

st.markdown(
    """
    ## Stating the Problem
    Approximately 20 billion tons, 2 billion tons, and 43 billion 
    tons of fresh produce are wasted and thrown away on farms, factories, 
    and stores, respectively due the the fact that they appear ugly yet 
    are perfectly edible. Minimizing this food waste could lead to the 
    minimization of food insecurity and mollify the severity of food deserts.

    ## Proposed Solution
    This is a two-pronged approach. First, an ML model will be used to detect 
    produce that is good (regardless of whether it appears ugly or not) using 
    image, color, shape, size, and texture data for individual produce items 
    on farms and factories (not necessary to do this for stores because it is 
    assumed that produce in stores is in good condition). Then, Volunteers can 
    see on an app the amount of produce and its location to be picked up 
    (whether it be a farm, factory, or store). The app will then direct them 
    to nearby drop off locations in food deserts or food banks.

    #### Solution Architecture Levels
    - At the level of PRODUCERS: Detect viable foods that are thrown away
    - At the level of MIDDLEMEN: Determine volunteers and efforts to reach consumers
    - At the level of CONSUMERS: Identify target communities 
    
    ### Relevant Sources
    - [The Problem of Food Waste](https://foodprint.org/issues/the-problem-of-food-waste/)
    - [From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)
    
"""
)