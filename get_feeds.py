import json
import os
import sys
import twitter

# The user of this script needs to add a twitter_auth.py file which 
# defines these variables
from twitter_auth import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

# This is based on an example from github.com/bear/python-twitter
def get_tweets(api, screen_name):
    sys.stdout.write('.')
    sys.stdout.flush()
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest = min(timeline, key=lambda x: x.id).id
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        tweets = api.GetUserTimeline(
            screen_name=screen_name,
            max_id=earliest,
            count=200)
        new_earliest = min(tweets, key=lambda x: x.id).id
        if not tweets or new_earliest == earliest:
            break
        else:
            earliest = new_earliest
            timeline += tweets
    return timeline

if __name__ == "__main__":
    api = twitter.Api(
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        sleep_on_rate_limit=True,
        tweet_mode='extended')
        
    sources = json.load(open('sources.json'))['sources']
    for source in sources:
        tweet_filename = 'twitter_feeds/' + source['id'] + '.json'
        if os.path.isfile(tweet_filename):
            print('File ' + tweet_filename + ' already exists, skipping...')
            continue
        print('Getting recent tweets for ' + source['human_name'])
        tweets = get_tweets(api, source['twitter_handle'])
        
        print('\nWriting tweets to disk...')
        tweet_file = open(tweet_filename, 'w')
        tweet_file.write('{ "tweets": [\n')
        for tweet in tweets:
            tweet_file.write(json.dumps(tweet._json, indent=2) + '\n')
            if tweet != tweets[-1]:
                tweet_file.write(',')
        tweet_file.write(']}')