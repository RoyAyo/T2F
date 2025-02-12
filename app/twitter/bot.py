import requests        

def get_tweet_text(tweet_url):
    try:
        url = f"https://proxy-jev0vg.fly.dev/tweet?url={tweet_url}"
        response = requests.get(url)
        tweet_text = response.text
        print("Tweet Text: ", tweet_text)
        return tweet_text
    except Exception as e:
        print("Error occured:", e)
        return None