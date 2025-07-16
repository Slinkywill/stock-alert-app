import yfinance as yf
import pandas_ta as ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Fetch data
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")
hist['SMA_50'] = ta.sma(hist['Close'], length=50)
hist['RSI_14'] = ta.rsi(hist['Close'], length=14)

# Target variable
hist['Target'] = (hist['Close'].shift(-1) > hist['Close']).astype(int)
hist = hist.dropna()

# Features & Scaling
features = ['Close', 'SMA_50', 'RSI_14']
X = hist[features]
y = hist['Target']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)

# Model training
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "trained_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model and scaler saved successfully.")

