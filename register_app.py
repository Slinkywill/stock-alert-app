import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY_JSON"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("Stock Alert Registration")

menu = st.sidebar.selectbox("Menu", ["Register", "Login"])

if menu == "Register":
    st.subheader("Create New Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    telegram_id = st.text_input("Telegram Chat ID")
    markets = st.multiselect("Select Markets", [
        "UK - FTSE", "US - NASDAQ", "Germany - DAX",
        "France - CAC", "Japan - Nikkei", "Crypto - Binance", "Commodities - CME"
    ])

    if st.button("Register"):
        try:
            user = auth.create_user(email=email, password=password)
            db.collection('users').document(email).set({
                'markets': markets,
                'telegram_id': telegram_id
            })
            st.success("Account created successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "Login":
    st.subheader("Login to Your Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        try:
            user_ref = db.collection('users').document(email).get()
            if user_ref.exists:
                st.success(f"Welcome, {email}!")
                user_data = user_ref.to_dict()
                st.write("Your Markets:", user_data.get('markets', []))
                st.write("Your Telegram ID:", user_data.get('telegram_id', 'Not Set'))
            else:
                st.error("User not found.")
        except Exception as e:
            st.error(f"Error: {e}")

