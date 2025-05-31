"""This module contains data about the home page"""

# Import necessary modules
import streamlit as st


def app(df, X, y):
    """This function creates the Data Info page"""

    # Add title to the page
    st.title("Data Info page")

    # Add subheader for the section
    st.subheader("View Data")

    # Create an expansion option to check the data
    with st.expander("View data"):
        st.dataframe(df)

    # Create a section to describe columns
    # Give subheader
    st.subheader("Columns Description:")

    # Create a checkbox to get the summary
    if st.checkbox("View Summary"):
        st.dataframe(df.describe())

    # Create multiple checkboxes in a row
    col_name, col_dtype, col_data = st.columns(3)

    # Show names of all dataframe columns
    with col_name:
        if st.checkbox("Column Names"):
            st.dataframe(df.columns)

    # Show datatypes of all columns
    with col_dtype:
        if st.checkbox("Columns Data Types"):
            dtypes = df.dtypes.apply(lambda x: x.name)
            st.dataframe(dtypes)
    
    # Show data for each column
    with col_data: 
        if st.checkbox("Columns Data"):
            col = st.selectbox("Column Name", list(df.columns))
            st.dataframe(df[col])
