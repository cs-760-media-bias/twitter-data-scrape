import json
import os

feed_path = 'twitter_feeds'
out_path = 'cleaned_tweets'

if __name__ == '__main__':
    for filename in os.listdir(feed_path):
        json_in = json.load(open(os.path.join(feed_path, filename)))
        screen_name = os.path.splitext(filename)[0].lower()
        print('Cleaning up tweet file ' + filename)

        user_out = None
        tweets_out = []
        for tweet in json_in['tweets']:
            user = tweet['user']
            if screen_name != user['screen_name'].lower():
                continue
            if user_out == None:
                user_out = {
                    'id': user['id'],
                    'screen_name': user['screen_name'].lower(),
                    'name': user['name'],
                    'description': user['description'],
                    'created_at': user['created_at'],
                    'followers_count': user['followers_count'],
                    'friends_count': user['friends_count'],
                    'listed_count': user['listed_count'],
                    'statuses_count': user['statuses_count']
                }

            tweet_out = {
                'id': tweet['id'],
                'created_at': tweet['created_at'],
                'text': tweet['full_text'],
                'hashtags': [],
                'user_mentions': [],
                'urls': [],
                'retweet_count': tweet['retweet_count'],
                'favorite_count': tweet['favorite_count'],
                'photo_count': 0,
                'video_count': 0,
                'reply_to_user_id': tweet['in_reply_to_user_id'],
                'reply_to_screen_name': tweet['in_reply_to_screen_name'],
                'reply_to_tweet_id': tweet['in_reply_to_status_id']
            }
            
            for hashtag in tweet['entities']['hashtags']:
                tweet_out['hashtags'].append(hashtag['text'])

            for user_mention in tweet['entities']['user_mentions']:
                user_mention_out = {
                    'id': user_mention['id'],
                    'screen_name': user_mention['screen_name'],
                    'name': user_mention['name']
                }
                tweet_out['user_mentions'].append(user_mention_out)
            
            for url in tweet['entities']['urls']:
                url_out = {
                    'url': url['url'],
                    'expanded_url': url['expanded_url']
                }
                tweet_out['urls'].append(url_out)

            if 'extended_entities' in tweet:
                if 'media' in tweet['extended_entities']:
                    for entity in tweet['extended_entities']['media']:
                        if entity['type'] == 'photo':
                            tweet_out['photo_count'] += 1
                        if entity['type'] == 'video':
                            tweet_out['video_count'] += 1
            
            tweets_out.append(tweet_out)

        if len(tweets_out) == 0:
            continue
        json_out = {
            'user': user_out,
            'tweets': tweets_out
        }
        out_filename = os.path.join(out_path, screen_name + '.json')
        with open(out_filename, 'w') as out_file:
            json.dump(json_out, out_file, indent=2)