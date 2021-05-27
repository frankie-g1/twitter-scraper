from utils.tweet import Tweet
import requests
import json
import logging


def get_tweets(query, count, proxy=None):
    if proxy is None:
        logging.basicConfig(format='%(asctime)s -> %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.warning('No proxy given, local network will be used -- be careful of getting banned.')
    # List of tweets
    tweets = []
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
            if proxy is not None:
                headers['x-guest-token'] = \
                    json.loads(s.post(proxies=proxy, headers=headers,
                                      url='https://api.twitter.com/1.1/guest/activate.json').content)[
                        'guest_token']
            else:
                headers['x-guest-token'] = \
                    json.loads(s.post(proxies=proxy, headers=headers,
                                      url='https://api.twitter.com/1.1/guest/activate.json').content)[
                        'guest_token']
        except:
            raise Exception('Request error trying to retrieve a guest token.')

        # Retrieve the last 20 tweets from the given query
        try:
            if proxy is not None:
                p = s.get(headers=headers,
                          proxies=proxy,
                          url=f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={query}&tweet_search_mode=live&count={count}&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel')
            else:
                p = s.get(headers=headers,
                          url=f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={query}&tweet_search_mode=live&count={count}&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel')

        except:
            raise Exception('Request error trying to retrieve the last 20 tweets.')

        # JSON data of all the tweets
        retrieved_tweets = p.json()['globalObjects']

        # Traverse the data and create Tweets
        for value in retrieved_tweets['tweets'].values():
            t = Tweet(
                timestamp=value['created_at'],
                tweet_id=value['id'],
                tweet_url=f"https://www.twitter.com/{retrieved_tweets['users'][value['user_id_str']]['screen_name']}/status/{value['id']}",
                username=retrieved_tweets['users'][value['user_id_str']]['name'],
                content=value['full_text'],
                user_id=value['user_id'],
                replies=value['reply_count'],
                retweets=value['retweet_count'],
                likes=value['favorite_count'],
                hashtags=[f"#{hashtag['text']}" for hashtag in value['entities']['hashtags']]
            )
            tweets.append(t)
    return tweets
