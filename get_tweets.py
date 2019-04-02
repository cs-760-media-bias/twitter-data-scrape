import json
import os
import sys
import twitter

FEED_PATH = 'tweets_raw'

# The user of this script needs to add a twitter_auth.py file which
# defines these variables
from twitter_auth import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


# This is based on an example from github.com/bear/python-twitter
def get_tweets(api, screen_name):
    sys.stdout.write('.')
    sys.stdout.flush()
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    if len(timeline) == 0:
        return timeline
    earliest = min(timeline, key=lambda x: x.id).id
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        tweets = api.GetUserTimeline(
            screen_name=screen_name,
            max_id=earliest,
            count=200)
        if len(tweets) == 0:
            return timeline
        new_earliest = min(tweets, key=lambda x: x.id).id
        if not tweets or new_earliest == earliest:
            break
        else:
            earliest = new_earliest
            timeline += tweets
    return timeline


if __name__ == '__main__':
    api = twitter.Api(
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        sleep_on_rate_limit=True,
        tweet_mode='extended')

    with open('sources.json') as sources_file:
        sources = json.load(sources_file)['sources']
    for source in sources:
        for handle in source['twitter_handles']:
            tweet_filename = os.path.join(FEED_PATH, handle + '.json')
            if os.path.isfile(tweet_filename):
                print('File ' + tweet_filename + ' already exists, skipping...')
                continue

            sys.stdout.write('Getting recent tweets for handle @' + handle)
            tweets = get_tweets(api, '@' + handle)

            print('\nWriting tweets to disk...')
            tweets_json = { 'tweets': [] }
            for tweet in tweets:
                tweets_json['tweets'].append(tweet._json)
            with open(tweet_filename, 'w') as tweet_file:
                json.dump(tweets_json, tweet_file, indent=2)
