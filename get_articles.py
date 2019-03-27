import json
import newspaper
import os
import sys


def get_article(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    sys.stdout.write('.')
    sys.stdout.flush()
    return {
        'url': article.url,
        'title': article.title,
        'authors': article.authors,
        'text': article.text,
    }


if __name__ == '__main__':
    sources = json.load(open('sources.json'))['sources']
    for source in sources:
        for handle in source['twitter_handles']:
            tweet_filename = 'twitter_feeds/' + handle + '.json'
            if not os.path.isfile(tweet_filename):
                print('No Twitter feed for @' + handle)
                continue
            tweets = json.load(open(tweet_filename))['tweets']

            article_filename = 'article_sources/' + handle + '.json'
            if os.path.isfile(article_filename):
                print('File ' + article_filename + ' already exists, skipping...')
                continue
            article_file = open(article_filename, 'w')

            article_file.write('{\n')
            sys.stdout.write('Getting article sources for @' + handle)
            for tweet in tweets:
                for url_entity in tweet['entities']['urls']:
                    url = url_entity['expanded_url']
                    article = None
                    try:
                        article = get_article(url)
                    except:
                        sys.stdout.write('!')
                        sys.stdout.flush()
                        continue
                    article_file.write(f'"{url}":\n')
                    article_file.write(json.dumps(article, indent=2))
                    if tweet != tweets[-1]:
                        article_file.write(',')
                    article_file.write('\n')
            article_file.write('}')
            article_file.close()
            sys.stdout.write('\n')
