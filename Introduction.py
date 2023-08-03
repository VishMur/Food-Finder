import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

global status

st.set_page_config(
    page_title="Introduction",
)

if 'log' not in st.session_state:
    st.session_state.log = 0


st.title("Food Finder")
st.write("A GNEC Hackathon Submission")

st.markdown(
    """
    ## Stating the Problem
    Approximately 20 billion tons, 2 billion tons, and 43 billion 
    tons of fresh produce are wasted and thrown away on farms, factories, 
    and stores, respectively due the the fact that they appear ugly yet 
    are perfectly edible. Minimizing this food waste could lead to the 
    minimization of food insecurity and mollify the severity of food deserts.

"""
)

add_vertical_space(1)
col1, col2 = st.columns(2)
col1.metric(label="Number of Food Deserts", value=6529)
col2.metric(label="Percent of of U.S Population in Food Deserts", value=14.47)

col3, col4 = st.columns(2)
col3.metric(label="Number of People in Food Deserts", value=23500000, delta=4700000, delta_color="inverse")
style_metric_cards()
add_vertical_space(1)

st.markdown(
    """
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

add_vertical_space(2)
st.markdown(
    """
    ## Sources
    - [[1] The Problem of Food Waste](https://foodprint.org/issues/the-problem-of-food-waste/)
    - [[2] From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)
    - [[3] Characteristics and Influential Factors of Food Deserts](https://www.ers.usda.gov/webdocs/publications/45014/30940_err140.pdf)
    - [[4] Food Deserts and Inequality](https://www.socialpolicylab.org/post/grow-your-blog-community)
    - [[5] Looking for oases in America's food deserts](https://www.farmprogress.com/commentary/looking-for-oases-in-america-s-food-deserts)
    - [[6] What Are Food Deserts and How Do We Solve Them?](https://www.edengreen.com/blog-collection/food-deserts)
    - [[7] USDA Food Access Atlas Documentation](https://www.ers.usda.gov/data-products/food-access-research-atlas/documentation/)
    - [From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)
    - [From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)
    - [From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)

"""
)
