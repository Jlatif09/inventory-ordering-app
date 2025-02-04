import streamlit as st
import pandas as pd
import io
import requests

# Load inventory data from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Jlatif09/inventory-ordering-app/main/COMPLETE%20VENDOR%20ITEMS%20FOR%20IVENTORY.xlsx"
    response = requests.get(url)
    if response.status_code == 200:
        file = io.BytesIO(response.content)
        df = pd.read_excel(file, sheet_name='VENDOR ITEMS FOR IVENTORY')
        df['Amount to Order'] = ""  # Placeholder column
        return df.sort_values(by=['Vendor', 'Vendor Item Name'])
    else:
        st.error("Failed to load the inventory file. Please check the file URL.")
        return pd.DataFrame()  # Return an empty dataframe if the file fails to load

df = load_data()

# Streamlit UI
st.title("Inventory Ordering System")

# Select vendor
vendors = df['Vendor'].unique()
selected_vendor = st.selectbox("Select Vendor", vendors)

# Filter data by selected vendor
filtered_df = df[df['Vendor'] == selected_vendor]

# Display and allow edits
edited_df = st.data_editor(filtered_df, num_rows="dynamic")

# Export updated file
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(edited_df)
st.download_button(
    "Download Updated Inventory",
    csv,
    "updated_inventory.csv",
    "text/csv",
    key='download-csv'
)

st.write("Use the table above to enter the amount needed to order and download the updated sheet.")
