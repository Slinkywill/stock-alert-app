import yfinance as yf
import pandas_ta as ta
import requests
from textblob import TextBlob
from pytrends.request import TrendReq
import praw

# --- Stock Data ---
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")
hist['SMA_50'] = ta.sma(hist['Close'], length=50)
hist['RSI_14'] = ta.rsi(hist['Close'], length=14)
print("Stock Data with Indicators:")
print(hist.tail())

# --- News Headlines with Sentiment ---
API_KEY = "39aba10d578249e89de2563e5a82b5be"
news_url = f"https://newsapi.org/v2/everything?q=Apple&language=en&sortBy=publishedAt&apiKey={API_KEY}"
news_response = requests.get(news_url).json()
print("\nLatest News Headlines & Sentiment:")
for article in news_response.get("articles", [])[:5]:
    headline = article['title']
    sentiment = TextBlob(headline).sentiment.polarity
    print(f"- {headline} | Sentiment: {sentiment:.2f}")

# --- Google Trends ---
pytrends = TrendReq()
pytrends.build_payload(["Apple"], timeframe='today 3-m')
trends_data = pytrends.interest_over_time()
print("\nGoogle Trends Data:")
print(trends_data.tail())

# --- Reddit Posts ---
reddit = praw.Reddit(
    client_id="8E_61IMGbZ2PVA-eKvJ2Nw",
    client_secret="VTVXkn8IYedEpWbPoLpqv2NLUef1MQ",
    user_agent="TradingSentimentApp"
)
print("\nTop Reddit Posts (r/stocks):")
for post in reddit.subreddit("stocks").hot(limit=5):
    print(f"- {post.title}")
