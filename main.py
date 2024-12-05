import streamlit as st
import pandas as pd
import io

def process_csv(file):
    # Load the CSV file
    data_df = pd.read_csv(file)

    # Identify boolean columns and count 'true' values
    boolean_columns = data_df.select_dtypes(include='bool').columns
    true_counts = data_df[boolean_columns].sum().reset_index()
    true_counts.columns = ['Company Type', 'Count of True']

    # Filter out non-zero counts and sort by count
    true_counts = true_counts[true_counts['Count of True'] > 0]
    sorted_counts = true_counts.sort_values(by='Count of True', ascending=False)

    return sorted_counts

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Streamlit app
st.title('CSV Processor: Count Boolean Values')

# File uploader
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])

if uploaded_file is not None:
    # Process the uploaded file
    sorted_counts = process_csv(uploaded_file)

    # Display the results
    st.subheader('Processed Data')
    st.dataframe(sorted_counts)

    # Provide download link for processed data
    csv_data = convert_df_to_csv(sorted_counts)
    st.download_button(
        label='Download Processed Data as CSV',
        data=csv_data,
        file_name='processed_data.csv',
        mime='text/csv',
    )
