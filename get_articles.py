import json
import os
import sys
from newspaper import Article

def get_article(url):
    sys.stdout.write('.')
    sys.stdout.flush()
    article = Article(url)
    article.download()
    article.parse()
    return { 
        'url': article.url,
        'title': article.title,
        'authors': article.authors,
        'text': article.text,
        'html': article.html
    }

if __name__ == '__main__':
    sources = json.load(open('sources.json'))['sources']
    for source in sources:
        tweet_filename = 'twitter_feeds/' + source['id'] + '.json'
        if not os.path.isfile(tweet_filename):
            print('No Twitter feed for ' + source['id'])
            continue
        article_filename = 'article_sources/' + source['id'] + '.json'
        if os.path.isfile(article_filename):
            print('File ' + article_filename + ' already exists, skipping...')
            continue
        article_file = open(article_filename, 'w+')
        article_file.write('{\n')
        tweets = json.load(open(tweet_filename))['tweets']
        print('Getting article sources for ' + source['human_name'])
        articles_json = {}
        for tweet in tweets:
            for url_entity in tweet['entities']['urls']:
                url = url_entity['expanded_url']
                article_file.write(f'"{url}":\n')
                article_file.write(json.dumps(get_article(url), indent=2))
                if tweet != tweets[-1]:
                    article_file.write(',')
                article_file.write('\n')
        article_file.write('}')