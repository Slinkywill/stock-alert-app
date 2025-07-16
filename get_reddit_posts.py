import praw

reddit = praw.Reddit(
    client_id="8E_61IMGbZ2PVA-eKvJ2Nw",
    client_secret="VTVXkn8IYedEpWbPoLpqv2NLUef1MQ",
    user_agent="TradingSentimentApp"
)

subreddit = reddit.subreddit("stocks")

for post in subreddit.hot(limit=5):
    print(f"- {post.title}")

