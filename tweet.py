class Tweet:

  def __init__(self, timestamp, tweet_id, tweet_url, username, content, user_id, replies, retweets, likes, hashtags):
    self.timestamp = timestamp
    self.tweet_id = tweet_id
    self.tweet_url = tweet_url
    self.username = username
    self.content = content
    self.user_id = user_id
    self.replies = replies
    self.retweets = retweets
    self.likes = likes
    self.hashtags = hashtags

  def __str__(self):
    return f'Timestamp:\n\t{self.timestamp}\n\t' \
           f'Tweet ID:\n\t\t{self.tweet_id}\n\t' \
           f'Tweet URL:\n\t\t{self.tweet_url}\n\t' \
           f'Username:\n\t\t{self.username}\n\t' \
           f'Content:\n\t\t{self.content}\n\t' \
           f'User ID:\n\t\t{self.user_id}\n\t' \
           f'Reply Count:\n\t\t{self.replies}\n\t' \
           f'Like Count:\n\t\t{self.likes}\n\t' \
           f'Hashtags:\n\t\t{self.hashtags}'

