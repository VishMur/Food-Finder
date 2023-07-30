# Imports
# -----------------------------------------------------------
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

application = get_wsgi_application()

from django_api.models import *

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from sklearn.cluster import KMeans





def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        user = authenticate(
            username=st.session_state["username"], password=st.session_state["password"]
        )

        if user is not None:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():

    sns.set_theme()
    # -----------------------------------------------------------

    # Helper functions
    # -----------------------------------------------------------
    # Load data from external source
    @st.cache
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