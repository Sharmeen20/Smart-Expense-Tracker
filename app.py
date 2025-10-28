
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "expenses_streamlit.csv"
valid_categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# Save new expense with user-selected date
def save_expense(date, amount, category, description):
    new_expense = pd.DataFrame({
        "Date": [date.strftime("%Y-%m-%d")],
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
    date = st.date_input("Date", datetime.now())  # 👈 New date picker added
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", valid_categories)
    description = st.text_input("Description")
    if st.button("Add Expense"):
        save_expense(date, amount, category, description)

elif choice == "View Summary":
    show_summary()

elif choice == "Export CSV":
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            st.download_button("Download CSV", f, file_name=DATA_FILE)
    else:
        st.info("No data to export.")

import streamlit as st
import speech_recognition as sr

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Please speak now...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.success("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, could not understand audio")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return ""

# Streamlit UI me button
if st.button("🎤 Use Voice to Add Description"):
    description = recognize_speech()
    st.session_state["description"] = description
``
