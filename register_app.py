import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin Init (for Firestore)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Firebase Web API Key
API_KEY = "AIzaSyAjvVuA0v8as-bFApZztE62bJUvO58dELQ"

st.title("Stock Alert App — Register & Login")

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    markets = st.multiselect("Select Markets", ["UK", "US", "Germany", "France", "Japan"])

    if st.button("Register"):
        if email and password:
            try:
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
                payload = {"email": email, "password": password, "returnSecureToken": True}
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    db.collection('users').document(email).set({"markets": markets})
                    st.success("Registration successful!")
                else:
                    st.error(f"Error: {res.json().get('error', {}).get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Exception: {e}")
        else:
            st.warning("Please enter email and password.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if email and password:
            try:
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
                payload = {"email": email, "password": password, "returnSecureToken": True}
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    st.success(f"Welcome, {email}!")
                    user_data = db.collection('users').document(email).get()
                    if user_data.exists:
                        st.write(f"Your Markets: {user_data.to_dict().get('markets', [])}")
                    else:
                        st.warning("No market preferences found.")
                else:
                    st.error(f"Error: {res.json().get('error', {}).get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Exception: {e}")
        else:
            st.warning("Please enter email and password.")

