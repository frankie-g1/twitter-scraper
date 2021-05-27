from utils.tweet import Tweet
import requests
import json
import logging
import random


def get_proxies():
    proxies = []
    with open('utils/proxies.txt') as f:
        for data in f.read().splitlines():
            tmp = data.split(':')
            proxies.append(tmp)
    return proxies

def get_tweets(query, count, proxy=None):
    # Uncomment out if you want to know that you aren't using a proxy -- gets a bit spammy
    # if proxy is None:
    #     logging.basicConfig(format='%(asctime)s -> %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    #     logging.warning('No proxy given, local network will be used -- be careful of getting banned.')
    if proxy is None:
        rand_proxy = random.choice(get_proxies())
        proxy = { 'https' : f'https://{rand_proxy[2]}:{rand_proxy[3]}@{rand_proxy[0]}:{rand_proxy[1]}' }
    # List of tweets
    tweets = []
    # Default headers
    # Authorization header is REQUIRED to retrieve a response
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "referrer": f"https://twitter.com/search?q={query}",
        "credentials": "include"
    }
    # Open a session
    with requests.Session() as s:
        # Run activate.json script to retrieve a guest token
        # Guest token is REQUIRED to retrieve a response
        try:
            if proxy is not None:
                req = s.post(proxies=proxy, headers=headers, url='https://api.twitter.com/1.1/guest/activate.json').content
                headers['x-guest-token'] = json.loads(req)['guest_token']
            else:
                req = s.post(headers=headers,
                             url='https://api.twitter.com/1.1/guest/activate.json').content
                headers['x-guest-token'] = json.loads(req)['guest_token']
        except Exception as e:
            raise Exception(f'Request error trying to retrieve a guest token.\nTraceback: {e}\nRequest Status Code: {req}')

        # Retrieve the last 20 tweets from the given query
        try:
            headers['cache-control'] = "no-cache"
            if proxy is not None:
                p = s.get(headers=headers,
                          proxies=proxy,
                          url=f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={query}&tweet_search_mode=live&count={count}&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel')
            else:
                p = s.get(headers=headers,
                          url=f'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={query}&tweet_search_mode=live&count={count}&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel')

        except Exception as e:
            raise Exception(f'Request error trying to retrieve the last 20 tweets.\nTraceback: {e}')

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
