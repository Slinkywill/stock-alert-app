import yfinance as yf
import pandas_ta as ta
import joblib
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load model and scaler
model = joblib.load("trained_model.pkl")
scaler = joblib.load("scaler.pkl")

# Telegram setup
TOKEN = "7952877655:AAHyuXkdc-7Nle-KkDPfIls07PMXiAT2Zko"
CHAT_ID = "6730579173"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Market groups with tickers
market_tickers = {
    "UK": ["BARC.L", "HSBA.L", "VOD.L", "BP.L", "SHEL.L"],
    "US": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "Germany": ["BMW.DE", "DAI.DE", "VOW3.DE"],
    "France": ["AIR.PA", "OR.PA", "SAN.PA"],
    "Japan": ["7203.T", "6758.T", "9984.T"]
}

# Get users and their selected markets
users_ref = db.collection('users').stream()

for user in users_ref:
    user_data = user.to_dict()
    user_markets = user_data.get('markets', [])
    report_lines = [f"Stock Predictions for {user.id}:\n"]

    tickers_to_check = []
    for market in user_markets:
        tickers_to_check.extend([(market, ticker) for ticker in market_tickers.get(market, [])])

    for market_name, ticker_symbol in tickers_to_check:
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="60d")
            hist['SMA_50'] = ta.sma(hist['Close'], length=50)
            hist['RSI_14'] = ta.rsi(hist['Close'], length=14)
            latest = hist.dropna().iloc[-1]

            features = ['Close', 'SMA_50', 'RSI_14']
            X_live = scaler.transform([latest[features]])
            prediction = model.predict(X_live)[0]

            signal = "BUY" if prediction == 1 else "SELL"

            company_name = ticker.info.get('longName', 'Unknown Company')
            report_lines.append(f"{market_name} {ticker_symbol} {company_name}: {signal}")

        except Exception as e:
            report_lines.append(f"{market_name} {ticker_symbol}: Error — {e}")

    # Send report via Telegram
    send_telegram("\n".join(report_lines))

    # Save report to file
    with open(f"{user.id}_predictions_report.txt", "w") as f:
        for line in report_lines:
            f.write(line + "\n")

