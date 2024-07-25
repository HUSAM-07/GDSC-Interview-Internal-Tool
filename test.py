import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)

# Connect to Google Sheet
spreadsheet = client.open("Interview_Dashboard")
sheet = spreadsheet.sheet1

# Test: Load data
data = sheet.get_all_records()
print(data)
