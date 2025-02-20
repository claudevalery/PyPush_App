import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler, LabelEncoder
from io import BytesIO

def remove_duplicates(df):
    return df.drop_duplicates()

def handle_missing_values(df, method="drop"):
    if method == "drop":
        return df.dropna()
    elif method == "mean":
        return df.fillna(df.mean(numeric_only=True))
    elif method == "median":
        return df.fillna(df.median(numeric_only=True))
    return df

def standardise_column_names(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

def correct_data_types(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    return df

def handle_outliers(df):
    z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
    return df[(z_scores < 3).all(axis=1)]

def ensure_data_integrity(df):
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all', axis=0)
    return df

def encode_categorical(df):
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col].astype(str))
    return df

def clean_data(df, tasks):
    if "Remove Duplicates" in tasks:
        df = remove_duplicates(df)
    if "Handle Missing Values" in tasks:
        method = st.selectbox("Select method for handling missing values:", ["drop", "mean", "median"], key='missing_values')
        df = handle_missing_values(df, method)
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

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def main():
    st.title("PyFlush: CSV Data Cleaning App")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Raw Data Preview")
        st.dataframe(df.head())

        cleaning_tasks = st.multiselect(
            "Select Cleaning Tasks", 
            ["Remove Duplicates", "Handle Missing Values", "Standardise Column Names", "Correct Data Types", "Handle Outliers", "Ensure Data Integrity", "Encode Categorical Variables"]
        )
        
        if st.button("Clean Data"):
            df_cleaned = clean_data(df, cleaning_tasks)
            st.write("### Cleaned Data Preview")
            st.dataframe(df_cleaned.head())
            
            cleaned_csv = convert_df_to_csv(df_cleaned)
            st.download_button(
                label="Download Cleaned CSV",
                data=cleaned_csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
