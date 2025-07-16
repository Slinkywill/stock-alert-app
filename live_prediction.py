import yfinance as yf
import pandas_ta as ta
import joblib

# Load saved model and scaler
model = joblib.load("trained_model.pkl")
scaler = joblib.load("scaler.pkl")

# Fetch latest data
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="60d")  # Last 60 days for indicators
hist['SMA_50'] = ta.sma(hist['Close'], length=50)
hist['RSI_14'] = ta.rsi(hist['Close'], length=14)
latest = hist.dropna().iloc[-1]

# Prepare features
features = ['Close', 'SMA_50', 'RSI_14']
X_live = scaler.transform([latest[features]])

# Make prediction
prediction = model.predict(X_live)[0]
if prediction == 1:
    print("🔵 Prediction: BUY Signal for AAPL")
else:
    print("🔴 Prediction: SELL Signal for AAPL")

