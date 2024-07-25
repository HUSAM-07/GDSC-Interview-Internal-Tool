import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)

# Connect to Google Sheet
spreadsheet = client.open("Interview_Dashboard")
sheet = spreadsheet.sheet1

# Function to load data from Google Sheets
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Function to update application status
def update_status(row_index, status):
    sheet.update_cell(row_index + 2, 4, status)  # Assuming the status column is the 4th column

# Streamlit UI
st.title("Recruitment Applications Management")

data = load_data()
if st.button("Refresh Data"):
    data = load_data()

# Display the data
st.dataframe(data)

# Application status update form
st.subheader("Update Application Status")
index = st.number_input("Application Row Index", min_value=0, max_value=len(data)-1, step=1)
status = st.selectbox("Status", ["Pending", "Reviewed", "Accepted", "Rejected"])

if st.button("Update Status"):
    update_status(index, status)
    st.success(f"Application status updated to '{status}' for row {index + 1}.")
    data = load_data()

# Display the updated data
st.dataframe(data)
