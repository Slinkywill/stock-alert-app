import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase from Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY_JSON"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("Stock Alert Dashboard")

email = st.text_input("Enter your registered email to see your latest predictions:")

if st.button("Show My Predictions"):
    try:
        with open(f"{email}_predictions_report.txt", "r") as f:
            lines = f.readlines()
        st.success("Here are your latest predictions:")
        for line in lines:
            st.write(line.strip())
    except FileNotFoundError:
        st.error("No prediction report found for this email.")
