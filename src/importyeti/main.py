import streamlit as st
import requests

# Define the list of data types
data_types = ["basic", "full", "shipments"]

# Define the URL for the API
url = "https://apis.importyeti.com/v1/organizations"

# Function to make the API request
def make_api_request(company_name, data_type):
    params = {
        "companyName": company_name,
        "data": data_type
    }
    response = requests.get(url, params=params)
    return response.json()

# Streamlit app code
def main():
    st.title("Company Data Lookup")

    # Company selection dropdown
    company_name = st.text_input("Enter Company Name:")
    
    # Data type selection dropdown
    data_type = st.selectbox("Select Data Type:", data_types)

    # Button to trigger API request
    if st.button("Fetch Data"):
        if company_name:
            response_data = make_api_request(company_name, data_type)
            st.write("Response:")
            st.write(response_data)
        else:
            st.warning("Please enter a company name")

if __name__ == "__main__":
    main()
