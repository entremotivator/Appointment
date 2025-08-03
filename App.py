import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="📅 CRM Appointments", layout="wide")
st.title("📅 CRM Appointment Manager")

# ---------- Configuration ----------
STATIC_SHEET_URL = "https://docs.google.com/spreadsheets/d/1LFfNwb9lRQpIosSEvV3O6zIwymUIWeG9L_k7cxw1jQs/edit#gid=0"

# ---------- Sidebar Authentication ----------
st.sidebar.header("🔐 Google Sheets Access")
json_file = st.sidebar.file_uploader("Upload your `service_account.json`", type="json")

st.sidebar.markdown("---")
st.sidebar.markdown("✅ Using static Google Sheet URL:")
st.sidebar.code(STATIC_SHEET_URL)

# ---------- Load Google Sheet Function ----------
@st.cache_data(show_spinner=True)
def load_gsheet_data(credentials):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(STATIC_SHEET_URL).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# ---------- Demo Fallback Data ----------
demo_data = pd.DataFrame([
    {
        "Email": "customallstars@gmail.com",
        "Guest Email": "customallstars@gmail.com",
        "Name": "Vietnamese Services",
        "Status": "confirmed",
        "Event ID": "7e62f941-c6f8-42c8-bf2b-fac739b2ded7",
        "Start Time (12hr)": "7/24/2025 1:00pm",
        "Start Time (24hr)": "7/24/2025 13:00",
        "Google Meet Link": "https://meet.google.com/kkp-htju-itz"
    },
    {
        "Email": "customallstars@gmail.com",
        "Guest Email": "customallstars@gmail.com",
        "Name": "Don Hudson",
        "Status": "confirmed",
        "Event ID": "d1b7ff1b-f4a1-4337-9416-928bb3f3b2ab",
        "Start Time (12hr)": "7/24/2025 2:00pm",
        "Start Time (24hr)": "7/24/2025 14:00",
        "Google Meet Link": "https://meet.google.com/ebj-ctqh-dxf"
    }
])

# ---------- Load Data ----------
if json_file:
    try:
        credentials = json_file.read()
        credentials_dict = eval(credentials.decode("utf-8"))
        df = load_gsheet_data(credentials_dict)
        st.success("✅ Live data loaded from Google Sheets.")
    except Exception as e:
        st.warning(f"⚠️ Could not load Google Sheet. Showing demo data.\n\nError: {e}")
        df = demo_data
else:
    st.info("📄 Upload credentials to view live data. Showing demo data.")
    df = demo_data

# ---------- Display Table ----------
st.subheader("📋 Appointments")
st.dataframe(df, use_container_width=True)

# ---------- Download Option ----------
st.download_button("⬇️ Download as CSV", df.to_csv(index=False), "appointments.csv", "text/csv")

# ---------- Footer ----------
st.markdown("---")
st.caption("🔧 Built with Streamlit · CRM Viewer")
