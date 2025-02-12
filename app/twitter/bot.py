import requests
from bs4 import BeautifulSoup

from app.utils.helper import convert_twitter_url_to_nitter

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://nitter.net/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

session = requests.Session()

def get_tweet_text(tweet_url):
    try:
        nitter_url = convert_twitter_url_to_nitter(tweet_url)
        response = session.get(nitter_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        tweet_text = soup.find("div", class_="tweet-content").text
        print("Tweet Text: ", tweet_text)
        return tweet_text
    except Exception as e:
        print("Error occured:", e)
        return None