import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.preprocessing import LabelEncoder
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
    
    # Dropdown for handling missing values
    if "Handle Missing Values" in cleaning_tasks:
        missing_value_method = st.selectbox(
            "Choose method for missing values:",
            ["Drop", "Mean", "Median"]
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

    # File Upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Raw Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Functions
        def remove_duplicates(df):
            return df.drop_duplicates()

        def handle_missing_values(df, method):
            if method == "Drop":
                return df.dropna()
            elif method == "Mean":
                return df.fillna(df.mean(numeric_only=True))
            elif method == "Median":
                return df.fillna(df.median(numeric_only=True))
            return df

        def standardise_column_names(df):
            df.columns = df.columns.str.lower().str.replace(" ", "_")
            return df

        def correct_data_types(df):
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric if possible
                except:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert to datetime if possible
                    except:
                        df[col] = df[col].astype(str)  # Force everything else to string
            return df

        def handle_outliers(df):
            num_df = df.select_dtypes(include=[np.number])  # Select numeric columns
            z_scores = np.abs(stats.zscore(num_df))
            df = df[(z_scores < 3).all(axis=1)]  # Remove rows with outliers
            return df

        def ensure_data_integrity(df):
            df = df.dropna(how='all', axis=1)  # Remove empty columns
            df = df.dropna(how='all', axis=0)  # Remove empty rows
            return df

        def encode_categorical(df):
            le = LabelEncoder()
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = le.fit_transform(df[col].astype(str))
            return df

        def clean_data(df, tasks, missing_value_method):
            """Applies selected cleaning tasks to the dataset"""
            if "Remove Duplicates" in tasks:
                df = remove_duplicates(df)
            if "Handle Missing Values" in tasks:
                df = handle_missing_values(df, missing_value_method)
            if "Standardise Column Names" in tasks:
                df = standardise_column_names(df)
            if "Correct Data Types" in tasks:
                df = correct_data_types(df)
            if "Handle Outliers" in tasks:
                df = handle_outliers(df)
            if "Ensure Data Integrity" in tasks:
                df = ensure_data_integrity(df)
            if "Encode Categorical Variables" in tasks:
                df = encode_categorical(df)
            return df

        # Button to Trigger Cleaning
        if st.button("Clean Data"):
            df_cleaned = clean_data(df, cleaning_tasks, missing_value_method)

            st.write("### Cleaned Data Preview")
            st.dataframe(df_cleaned.head())  # Show cleaned dataset

            cleaned_csv = df_cleaned.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Cleaned CSV",
                data=cleaned_csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
