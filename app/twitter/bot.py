import requests
from bs4 import BeautifulSoup

tweet_url = "https://nitter.net/roy_ay0/status/1889417355341520920"

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
        response = session.get(tweet_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        tweet_text = soup.find("div", class_="tweet-content").text
        return tweet_text
    except Exception as e:
        print(e)
        return None