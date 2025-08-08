import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# ---------- Config ----------
SHEET_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
STATIC_SHEET_URL = "https://docs.google.com/spreadsheets/d/1LFfNwb9lRQpIosSEvV3O6zIwymUIWeG9L_k7cxw1jQs/edit?gid=0#gid=0"
DEFAULT_CREDENTIALS_FILE = "service_account.json"  # Local file path

# ---------- Sidebar Navigation ----------
def sidebar_navigation():
    st.sidebar.header("🔐 Google Sheets Access")
    json_file = st.sidebar.file_uploader("Upload your `service_account.json`", type="json")
    
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["📋 Dashboard", "📅 Appointments", "👥 Contacts", "🎯 Leads", "📈 Analytics", "⚙️ Settings"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("✅ **Data Source:**")
    st.sidebar.code(STATIC_SHEET_URL, language="text")
    
    return json_file, page

# ---------- Load Google Sheets Data ----------
@st.cache_data(show_spinner=True)
def load_gsheet_data(credentials_dict):
    try:
        required_keys = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id"]
        if not all(key in credentials_dict for key in required_keys):
            raise ValueError("Invalid credentials file. Required keys are missing.")

        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SHEET_SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(STATIC_SHEET_URL).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Error loading Google Sheets data: {e}")
        return None

# ---------- Main ----------
json_file, page = sidebar_navigation()

if json_file:
    try:
        credentials_dict = json.load(json_file)
        df = load_gsheet_data(credentials_dict)
        if df is not None:
            st.success("✅ Google Sheets data loaded successfully!")
            st.dataframe(df)
    except json.JSONDecodeError:
        st.error("❌ Uploaded file is not valid JSON.")
else:
    try:
        with open(DEFAULT_CREDENTIALS_FILE, "r") as f:
            credentials_dict = json.load(f)
        df = load_gsheet_data(credentials_dict)
        if df is not None:
            st.info("📄 Loaded data from default service_account.json")
            st.dataframe(df)
    except FileNotFoundError:
        st.warning("📤 Please upload your `service_account.json` file to load data.")
