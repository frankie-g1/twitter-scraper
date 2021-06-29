class Tweet:

    def __init__(self, timestamp, tweet_id, tweet_url, username, content, user_id, replies, retweets, likes, hashtags, emotion):
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
        self.emotion = emotion

    def __str__(self):
        return f'Timestamp:\n\t{self.timestamp}\n\t' \
               f'Tweet ID:\n\t\t{self.tweet_id}\n\t' \
               f'Tweet URL:\n\t\t{self.tweet_url}\n\t' \
               f'Username:\n\t\t{self.username}\n\t' \
               f'Content:\n\t\t{self.content}\n\t' \
               f'User ID:\n\t\t{self.user_id}\n\t' \
               f'Reply Count:\n\t\t{self.replies}\n\t' \
               f'Like Count:\n\t\t{self.likes}\n\t' \
               f'Hashtags:\n\t\t{self.hashtags}' \
               f'Emotion:\n\t\t{self.emotion}'

    def one_line(self):
        return ""

    def to_json(self):
        return {
            'timestamp': self.timestamp,
            'tweet_id': self.tweet_id,
            'tweet_url': self.tweet_url,
            'username': self.username,
            'content': self.content,
            'user_id': self.user_id,
            'reply_count': self.replies,
            'like_count': self.likes,
            'hashtags': [h for h in self.hashtags],
            'emotion': self.emotion
        }
