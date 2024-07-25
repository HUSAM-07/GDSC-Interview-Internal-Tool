import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import altair as alt

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = "credentials/google_sheets_credentials.json"  # Path to your credentials JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Connect to Google Sheet
spreadsheet = client.open("Interview_Dashboard")
sheet = spreadsheet.sheet1

# Function to load data from Google Sheets
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Function to update application status for a specific row
def update_status(row_index, status):
    sheet.update_cell(row_index + 2, 4, status)  # Assuming the status column is the 4th column

# Function to bulk update application status
def bulk_update_status(start_row, end_row, status):
    for i in range(start_row, end_row + 1):
        update_status(i, status)

# Streamlit UI
st.title("Google DSC's Internal Recruitment Applications Management Tool")
st.warning("This tool is exclusively made for GDSC's Internal Teams | Not for Public Access")

# Sidebar for filtering and bulk updates
with st.sidebar:
    st.header("Filter and Bulk Update")

    # Search feature
    search_name = st.text_input("Search by Applicant Name")

    # Bulk update section
    with st.expander("Bulk Update Application Status"):
        start_row = st.number_input("Start Row Index", min_value=0, max_value=1000, step=1)
        end_row = st.number_input("End Row Index", min_value=0, max_value=1000, step=1)
        bulk_status = st.selectbox("Status for Bulk Update", ["Pending", "Reviewed", "Accepted", "Rejected"])

        if st.button("Bulk Update Status"):
            if start_row <= end_row:
                bulk_update_status(start_row, end_row, bulk_status)
                st.success(f"Bulk update applied: Status set to '{bulk_status}' from row {start_row + 1} to row {end_row + 1}.")
            else:
                st.error("Start row must be less than or equal to end row.")

# Load and filter data
data = load_data()

if search_name:
    data = data[data["Applicant Name"].str.contains(search_name, case=False, na=False)]

if st.sidebar.button("Refresh Data"):
    data = load_data()
    if search_name:
        data = data[data["Applicant Name"].str.contains(search_name, case=False, na=False)]

# Main content area
st.dataframe(data)

# Application status update form
st.subheader("Update Application Status")
index = st.number_input("Application Row Index", min_value=0, max_value=len(data)-1, step=1)
status = st.selectbox("Status", ["Pending", "Reviewed", "Accepted", "Rejected"])

if st.button("Update Status"):
    update_status(index, status)
    st.success(f"Application status updated to '{status}' for row {index + 1}.")
    data = load_data()
    if search_name:
        data = data[data["Applicant Name"].str.contains(search_name, case=False, na=False)]

# Visualization feature
st.subheader("Applications by Team Preference")
if "Team" in data.columns:
    team_counts = data["Team"].value_counts().reset_index()
    team_counts.columns = ["Team", "Count"]

    chart = alt.Chart(team_counts).mark_bar().encode(
        x='Team',
        y='Count',
        color='Team'
    ).properties(
        title='Number of Applications by Team Preference'
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("The 'Team' column is not present in the data.")
