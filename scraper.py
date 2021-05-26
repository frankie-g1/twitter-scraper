from tweet import Tweet


class Scraper:

    tweets = []

    def get_tweets(self):
        import requests
        import json

        # Default headers
        # Authorization header is REQUIRED to retrieve a response
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "referrer": "https://twitter.com/search?q=btc",
            "credentials": "include"
        }
        # Open a session
        with requests.Session() as s:
            # Run activate.json script to retrieve a guest token
            # Guest token is REQUIRED to retrieve a response
            try:
                headers['x-guest-token'] = \
                json.loads(s.post(headers=headers, url='https://api.twitter.com/1.1/guest/activate.json').content)[
                    'guest_token']
            except:
                raise Exception('Request error trying to retrieve a guest token.')

            # Retrieve the last 20 tweets from the given query
            try:
                p = s.get(headers=headers,
                          url="https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=btc&count=20&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel")
            except:
                raise Exception('Request error trying to retrieve the last 20 tweets.')

            retrieved_tweets = p.json()['globalObjects']

            for key, value in retrieved_tweets['tweets'].items():
                t = Tweet(
                    timestamp=value['created_at'],
                    tweet_id=value['id'],
                    tweet_url=None,
                    username=retrieved_tweets['users'][value['user_id_str']]['name'],
                    content=value['full_text'],
                    user_id=value['user_id'],
                    replies=value['reply_count'],
                    retweets=value['retweet_count'],
                    likes=value['favorite_count'],
                    hashtags=None
                )

                self.tweets.append(t)


if __name__ == "__main__":
    scraper = Scraper()
    scraper.get_tweets()

    for t in scraper.tweets:
        print(t)
