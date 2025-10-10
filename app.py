
import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "expenses_streamlit.csv"

# Valid categories
valid_categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# Save new expense
def save_expense(amount, category, description):
    new_expense = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Amount": [amount],
        "Category": [category],
        "Description": [description]
    })
    data = load_data()
    data = pd.concat([data, new_expense], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)
    st.success("Expense added successfully!")

# Show summary
def show_summary():
    data = load_data()
    if data.empty:
        st.info("No expenses recorded yet.")
    else:
        summary = data.groupby("Category")["Amount"].sum()
        st.subheader("Expense Summary by Category")
        st.bar_chart(summary)

# Streamlit UI
st.title("Smart Expense Tracker")

menu = ["Add Expense", "View Summary", "Export CSV"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("Add a New Expense")
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", valid_categories)
    description = st.text_input("Description")
    if st.button("Add Expense"):
        save_expense(amount, category, description)

elif choice == "View Summary":
    show_summary()

elif choice == "Export CSV":
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            st.download_button("Download CSV", f, file_name=DATA_FILE)
    else:
        st.info("No data to export.")
