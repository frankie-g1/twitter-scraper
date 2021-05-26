class Tweet:

  def __init__(self, timestamp, tweet_id, tweet_url, username, user_id, replies, retweets, likes, hashtags, urls, photos):
    self.timestamp = timestamp
    self.tweet_id = tweet_id
    self.tweet_url = tweet_url
    self.username = username
    self.user_id = user_id
    self.replies = replies
    self.retweets = retweets
    self.likes = likes
    self.hashtags = hashtags
    self.urls = urls
