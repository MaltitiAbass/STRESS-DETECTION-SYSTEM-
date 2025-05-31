"""This module contains data about the home page"""

# Import necessary modules
import streamlit as st

def app(df, X, y):
    """This function creates the home page"""
    
    # Add title to the home page
    st.title("Acquah StressPredict")

    # Add image to the home page
    st.image("./images/home.png")

    # Add brief description of your web app
    st.markdown(
    """<p style="font-size:20px;">
           Acquah StressPredict is a web application designed to detect stress using machine learning. It offers three methods for stress analysis: manual input of data, uploading images and real-time video capture. The system provides accurate stress predictions and insights through a user-friendly interface, making it easier to manage and understand stress levels.
        </p>
    """, unsafe_allow_html=True)

   
