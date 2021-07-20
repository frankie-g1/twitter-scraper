from utils.scraper import get_tweets
import threading
import time
import json

queue = []


def post_to_database(query, t):
    db = firebase.FirebaseApplication("INSERT FIREBASE URL HERE", None)
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
    db.put(f'/twitter/queries/{query}/{t.timestamp}', name="emotion", data=t.emotion)


def write_to_file(query, t):
    with open(r'C:\Users\guarinof\PycharmProjects\twitter-scraper\tweets.json', 'a') as f:
        json.dump(t.to_json(), f)
        f.write('\n')


def post_queue():
    start_time = time.time()

    # Queue based processing
    # Use 5 threads to process through the posting of the data to the database
    # WE DO THIS TO NOT OVERHEAT AND OVERUSE THe RASPBERRY PI CPU
    while queue:
        threads = []
        if len(queue) < 5:
            for i in range(len(queue)):
                x = threading.Thread(target=write_to_file, args=queue.pop(0))
                threads.append(x)
                x.start()
        else:
            for i in range(5):
                x = threading.Thread(target=write_to_file, args=queue.pop(0))
                threads.append(x)
                x.start()
        for t in threads:
            t.join()
    print("Posting to database took --- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    tweets = []
    query = 'btc'
    while True:
        start_time = time.time()
        # Get tweets and process them
        for t in get_tweets(query=query, count=20):
            if t.tweet_id not in tweets:
                tweets.append(t.tweet_id)
                # Add to queue
                write_to_file(query, t)
                # queue.append([query, t])
        # Start queue processing
        # threading.Thread(target=post_queue).start()

        print("Checking tweets took --- %s seconds ---" % (time.time() - start_time))

        # Make sure the memory of the tweets we compare isn't too big to compare
        if len(tweets) > 40:
            del tweets[0:20]

        time.sleep(60)
