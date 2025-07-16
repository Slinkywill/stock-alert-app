import requests
from textblob import TextBlob

API_KEY = "39aba10d578249e89de2563e5a82b5be"
query = "Apple"
url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

for article in data.get("articles", [])[:5]:
    headline = article['title']
    blob = TextBlob(headline)
    sentiment = blob.sentiment.polarity  # Range: -1 (negative) to +1 (positive)
    print(f"- {headline} | Sentiment Score: {sentiment:.2f}")


