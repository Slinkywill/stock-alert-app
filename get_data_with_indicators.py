import yfinance as yf
import pandas_ta as ta

ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")

hist['SMA_50'] = ta.sma(hist['Close'], length=50)
hist['RSI_14'] = ta.rsi(hist['Close'], length=14)

print(hist.tail())


