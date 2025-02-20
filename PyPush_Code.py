import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler, LabelEncoder
from io import BytesIO

# Set page title and layout
st.set_page_config(page_title="PyFlush - Data Cleaning", layout="wide")

# Display Logo
st.image("PyFl_Logo.png", width=200)

# Sidebar Menu
with st.sidebar:
    st.title("PyFlush")
    st.subheader("Navigation")
    page = st.radio("Go to:", ["Home", "FAQ", "Terms & Conditions", "Privacy Policy"])
    
    st.subheader("Data Cleaning Options")
    cleaning_tasks = st.multiselect(
        "Select Cleaning Tasks", 
        ["Remove Duplicates", "Handle Missing Values", "Standardise Column Names", "Correct Data Types", 
         "Handle Outliers", "Ensure Data Integrity", "Encode Categorical Variables"]
    )

# Page Navigation Logic
if page == "FAQ":
    st.title("Frequently Asked Questions")
    st.write("Here you can answer common questions...")
elif page == "Terms & Conditions":
    st.title("Terms & Conditions")
    st.write("Your terms and conditions go here...")
elif page == "Privacy Policy":
    st.title("Privacy Policy")
    st.write("Your privacy policy goes here...")
else:
    # Main Data Cleaning App
    st.title("PyFlush: CSV Data Cleaning App")
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Raw Data Preview")
        st.dataframe(df.head())

        if st.button("Clean Data"):
            # Implement cleaning functions based on user selection
            st.write("### Cleaned Data Preview")
            st.dataframe(df.head())  # Just a placeholder

            cleaned_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Cleaned CSV",
                data=cleaned_csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
