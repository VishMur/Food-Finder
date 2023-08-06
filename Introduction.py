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
    and stores, respectively¹ due the the fact that they appear ugly yet 
    are perfectly edible. Minimizing this food waste could lead to less
    food insecurity and mollify the severity of food deserts (entire areas
    lacking access to fresh produce due to a dearth of local stores)².
"""
)

add_vertical_space(1)
col1, col2 = st.columns(2)
col1.metric(label="Number of Food Deserts³", value="6.5K+")
col2.metric(label="Number of Americans in Food Deserts⁴", value="23.5M", delta="4.7M/yr", delta_color="inverse")

col3, col4 = st.columns(2)
col3.metric(label="Percent of U.S Population in Food Deserts⁴", value=7.07, delta="1.41/yr", delta_color="inverse")
col4.metric(label="Percent of Americans in Food Insecurity⁴", value=16.26)
style_metric_cards()
add_vertical_space(1)

st.markdown(
    """
    ### UN Sustainable Development Goals (SDGs)
    These dual social problems of food deserts and food waste are related to two
    important UN Goals:
    """
)

st.image("https://raw.githubusercontent.com/VishMur/Food-Finder/main/img_assets/UN%20Goals%20Focus.png")

st.markdown(
    """
    ##### Goal 2: Zero Hunger
    - **Target 2.1:** 
    
    """
)

col1, col2 = st.columns([1, 30])

with col2:
    st.write("""
    By 2030, end hunger and ensure access by all people, 
    in particular the poor and people in vulnerable situations, 
    including infants, to safe, nutritious and sufficient food all year round.
    """)

st.markdown("""

    ##### Goal 12: Responsible Consumption and Production
    - **Target 12.3:** 
    
    """
)

col1, col2 = st.columns([1, 30])

with col2:
    st.write("""
    By 2030, halve per capita global food waste at the 
    retail and consumer levels and reduce food losses along
    production and supply chains, including post-harvest losses.
    """)

st.markdown(
    """
    ## Proposed Solution
    Ugly produce is a type of produce that is wasted not because of bad taste or
    a lack of nutritiousness but because it does not meet consumers' shape or color
    expectations⁵. While such food would not sell in stores in non-food desert areas,
    It would be very useful to food insecure people or people living in food deserts.
    
    Networks of volunteers are already working to pick up wasted produce from farms 
    and factories⁶, but they lack an application or website to quickly provide them information
    about where to go to maximize their productivity by finding large amounts of ugly produce.
    This is important because fresh produce tends to decay quickly, and can only be donated for so long.
    
    Our approach is two-pronged. First, an machine learning model will be used to detect 
    produce that is good, ugly (acceptable), or bad using image, color, shape, size, and
    texture data for individual produce items at producer locations (typically farms).
    Then, volunteers can see, on this web application, producers' locations and the number
    of batches of ugly produce they have to be picked up and donated
    (whether it be a farm, factory, or store). The app will also show them 
    nearby food banks delivering food to food insecure people and/or those living in food deserts.

    #### Solution Architecture Level Summary
    - At the level of PRODUCERS: Detect viable foods that are thrown away
    - At the level of MIDDLEMEN: Allow volunteers to find producers with ugly produce and consumers needing food
    - At the level of CONSUMERS: Identify target communities for food distribution
"""
)

add_vertical_space(2)
st.markdown(
    """
    ## Sources
    1. [The Problem of Food Waste](https://foodprint.org/issues/the-problem-of-food-waste/)
    2. [USDA Food Access Atlas Documentation](https://www.ers.usda.gov/data-products/food-access-research-atlas/documentation/)
    3. [Understanding America’s Rural and Urban Food Deserts](https://www.bayer.com/en/us/news-stories/understanding-americas-rural-and-urban-food-deserts#:~:text=There%20are%20over%206%2C500%20food,refrigerators%20often%20look%20the%20same.)
    4. [Food Deserts and Inequality](https://www.socialpolicylab.org/post/grow-your-blog-community)
    5. [Seeing Beauty in Ugly Produce: A Food Waste Perspective](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4349504)
    6. [From field to fork: the six stages of wasting food](https://amp.theguardian.com/environment/2016/jul/14/from-field-to-fork-the-six-stages-of-wasting-food)
"""
)
