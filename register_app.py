import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

# Firebase Admin Init
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Pyrebase Config (for client-side login)
firebaseConfig = {
    "apiKey": "AIzaSyAjvVuA0v8as-bFApZztE62bJUvO58dELQ",
    "authDomain": "stockalertsapp-2b838.firebaseapp.com",
    "projectId": "stockalertsapp-2b838",
    "storageBucket": "stockalertsapp-2b838.appspot.com",
    "messagingSenderId": "106920059046223708495",
    "appId": "1:106920059046223708495:web:abcdefg1234567",
    "measurementId": "G-XYZ12345",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
pb_auth = firebase.auth()

st.title("Stock Alert Registration & Login")

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    markets = st.multiselect("Select Markets", ["UK", "US", "Germany", "France", "Japan"])

    if st.button("Register"):
        try:
            user = auth.create_user(email=email, password=password)
            db.collection('users').document(email).set({"markets": markets})
            st.success("Account created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Login":
    st.subheader("Login to Your Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        try:
            user = pb_auth.sign_in_with_email_and_password(email, password)
            st.success(f"Welcome, {email}!")

            user_data = db.collection('users').document(email).get()
            if user_data.exists:
                markets = user_data.to_dict().get('markets', [])
                st.write(f"Your selected markets: {markets}")
            else:
                st.warning("No market preferences found for this account.")

        except Exception as e:
            st.error(f"Login failed: {e}")

