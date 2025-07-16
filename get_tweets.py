import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFNP3AEAAAAAokUU9by3L2Eitd20K3iux9JeQsA%3DyhOjs9fO6L2XOLEkDxY27X3PFfglmYSF3n3JtdTJTau77nSmnm"
query = "news"
url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=5&tweet.fields=text"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

response = requests.get(url, headers=headers)
data = response.json()

for tweet in data.get("data", []):
    print(f"- {tweet['text']}")
import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFNP3AEAAAAAokUU9by3L2Eitd20K3iux9JeQsA%3DyhOjs9fO6L2XOLEkDxY27X3PFfglmYSF3n3JtdTJTau77nSmnm"
query = "Apple"
url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=5&tweet.fields=text"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

response = requests.get(url, headers=headers)
data = response.json()

for tweet in data.get("data", []):
    print(f"- {tweet['text']}")

