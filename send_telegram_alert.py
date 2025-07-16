import requests

TOKEN = "7952877655:AAHyuXkdc-7Nle-KkDPfIls07PMXiAT2Zko"
CHAT_ID = "6730579173"
MESSAGE = "🔔 Test Alert — Your Telegram Bot is Working!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": MESSAGE
}

response = requests.post(url, data=data)
print("Status:", response.status_code)
print("Response:", response.json())

