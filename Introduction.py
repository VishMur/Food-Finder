# Imports
# -----------------------------------------------------------
import os
from django.core.wsgi import get_wsgi_application
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from django.contrib.auth import authenticate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

from django_api.models import *

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from sklearn.cluster import KMeans

from pages.Django_Login import check_password

def display_introduction():
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

if check_password():
    display_introduction()

if 5 == 6:

    sns.set_theme()
    # -----------------------------------------------------------

    # Helper functions
    # -----------------------------------------------------------
    # Load data from external source
    @st.cache_data
    def load_data():
        df = pd.read_csv(
            "https://raw.githubusercontent.com/ThuwarakeshM/PracticalML-KMeans-Election/master/voters_demo_sample.csv"
        )
        return df

    df = load_data()

    def run_kmeans(df, n_clusters=2):
        kmeans = KMeans(n_clusters, random_state=0).fit(df[["Age", "Income"]])

        fig, ax = plt.subplots(figsize=(16, 9))

        ax.grid(False)
        ax.set_facecolor("#FFF")
        ax.spines[["left", "bottom"]].set_visible(True)
        ax.spines[["left", "bottom"]].set_color("#4a4a4a")
        ax.tick_params(labelcolor="#4a4a4a")
        ax.yaxis.label.set(color="#4a4a4a", fontsize=20)
        ax.xaxis.label.set(color="#4a4a4a", fontsize=20)
        # --------------------------------------------------

        # Create scatterplot
        ax = sns.scatterplot(
            ax=ax,
            x=df.Age,
            y=df.Income,
            hue=kmeans.labels_,
            palette=sns.color_palette("colorblind", n_colors=n_clusters),
            legend=None,
        )

        # Annotate cluster centroids
        for ix, [age, income] in enumerate(kmeans.cluster_centers_):
            ax.scatter(age, income, s=200, c="#a8323e")
            ax.annotate(
                f"Cluster #{ix+1}",
                (age, income),
                fontsize=25,
                color="#a8323e",
                xytext=(age + 5, income + 3),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#a8323e", lw=2),
                ha="center",
                va="center",
            )

        return fig

    # -----------------------------------------------------------

    # SIDEBAR
    # -----------------------------------------------------------
    sidebar = st.sidebar
    df_display = sidebar.checkbox("Display Raw Data", value=True)

    n_clusters = sidebar.slider(
        "Select Number of Clusters",
        min_value=2,
        max_value=10,
    )

    sidebar.write(
        """
        Hey friend!It seems we have lots of common interests. 
        I'd love to connect with you on 
        - [LinkedIn](https://linkedin.com/in/thuwarakesh/)
        - [Twitter](https://www.twitter.com/thuwarakesh/)
        And please follow me on [Medium](https://thuwarakesh.medium.com/), because I write about data science.
        """
    )
    # -----------------------------------------------------------

    # Main
    # -----------------------------------------------------------
    # Create a title for your app
    st.title("Interactive K-Means Clustering")
    """
    An illustration by [Thuwarakesh Murallie](https://thuwarakesh.medium.com) for the Streamlit introduction article on Medium.
    """

    entity = Entity.objects.first()
    st.write(entity.phone_number)
    st.write(entity.latitude)
    st.write(entity.longitude)
    st.write(entity.address)

    # Show cluster scatter plot
    st.write(run_kmeans(df, n_clusters=n_clusters))

    if df_display:
        st.write(df)
    # -----------------------------------------------------------