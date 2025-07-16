import streamlit as st
import yfinance as yf
import pandas_ta as ta
import joblib

st.title("Stock Buy/Sell Predictor")

ticker_input = st.text_input("Enter Stock Ticker (e.g. AAPL):", value="AAPL")

if st.button("Predict"):
    try:
        model = joblib.load("trained_model.pkl")
        scaler = joblib.load("scaler.pkl")

        ticker = yf.Ticker(ticker_input)
        hist = ticker.history(period="60d")
        hist['SMA_50'] = ta.sma(hist['Close'], length=50)
        hist['RSI_14'] = ta.rsi(hist['Close'], length=14)
        latest = hist.dropna().iloc[-1]

        features = ['Close', 'SMA_50', 'RSI_14']
        X_live = scaler.transform([latest[features]])

        prediction = model.predict(X_live)[0]

        if prediction == 1:
            st.success(f"🔵 BUY Signal for {ticker_input}")
        else:
            st.error(f"🔴 SELL Signal for {ticker_input}")

    except Exception as e:
        st.warning(f"Error: {e}")

