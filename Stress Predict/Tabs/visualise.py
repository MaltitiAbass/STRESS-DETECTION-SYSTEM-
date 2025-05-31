"""This module contains data about the visualisation page"""

# Import necessary modules
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
import streamlit as st

# Import necessary functions from web_functions
from web_functions import train_model

def app(df, X, y):
    """This function creates the visualisation page"""
    
    # Remove the warnings
    warnings.filterwarnings('ignore')

    # Set the page title
    st.title("Visualise the Stress Level")

    # Create a checkbox to show correlation heatmap
    if st.checkbox("Show the correlation heatmap"):
        st.subheader("Correlation Heatmap")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.iloc[:, 1:].corr(), annot=True, ax=ax)   # Creating a seaborn heatmap
        bottom, top = ax.get_ylim()                             # Adjusting margin limits
        ax.set_ylim(bottom + 0.5, top - 0.5)
        st.pyplot(fig)

    # Create a checkbox to show scatter plots
    if st.checkbox("Show Scatter Plot"):
        st.subheader("Scatter Plots")

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        sns.scatterplot(ax=axes[0, 0], data=df, x='bt', y='rr')
        axes[0, 0].set_title("Body Temperature vs Respiration Rate")

        sns.scatterplot(ax=axes[0, 1], data=df, x='sr', y='lm')
        axes[0, 1].set_title("Snoring Rate vs Limb Movement")

        sns.scatterplot(ax=axes[1, 0], data=df, x='bo', y='bt')
        axes[1, 0].set_title("Blood Oxygen vs Body Temperature")

        sns.scatterplot(ax=axes[1, 1], data=df, x='sh', y='hr')
        axes[1, 1].set_title("Sleeping Hours vs Heart Rate")

        st.pyplot(fig)

    # Create a checkbox to display boxplot
    if st.checkbox("Display Boxplot"):
        st.subheader("Boxplots")

        fig, ax = plt.subplots(figsize=(15, 5))
        df.boxplot(['sr', 'rr', 'bt', 'rem', 'bo', 'sh'], ax=ax)
        st.pyplot(fig)

    # Create a checkbox to show sample results in a pie chart
    if st.checkbox("Show Sample Results"):
        st.subheader("Sample Results")

        safe = (df['sl'] == 0).sum()
        low = (df['sl'] == 1).sum()
        med = (df['sl'] == 2).sum()
        high = (df['sl'] == 3).sum()
        vhigh = (df['sl'] == 4).sum()
        data = [safe, low, med, high, vhigh]
        labels = ['Safe', 'Low', 'Medium', 'High', 'Very High']
        colors = sns.color_palette('pastel')[0:5]
        fig, ax = plt.subplots()
        ax.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
        st.pyplot(fig)
