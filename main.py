from utils.scraper import get_tweets

if __name__ == "__main__":
    for t in get_tweets(query='btc', count=20):
        pass
        # print(t.to_json())