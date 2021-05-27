from utils.scraper import get_tweets
from firebase import firebase
import threading


def post_to_database(query, t):
    db = firebase.FirebaseApplication("INSERT_URL_HERE", None)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="timestamp", data=t.timestamp)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="tweet_id", data=t.tweet_id)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="tweet_url", data=t.tweet_url)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="username", data=t.username)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="content", data=t.content)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="user_id", data=t.user_id)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="replies", data=t.replies)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="retweets", data=t.retweets)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="likes", data=t.likes)
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="hashtags", data=t.hashtags)


if __name__ == "__main__":
    tweets = []
    query = 'btc'
    while True:
        new = False
        threads = []
        for t in get_tweets(query=query, count=20):
            if t.tweet_id not in tweets:
                tweets.append(t.tweet_id)
                x = threading.Thread(target=post_to_database, args=(query, t))
                threads.append(x)
                x.start()
        for t in threads:
            t.join()
        if len(tweets) > 40:
            del tweets[0:20]
