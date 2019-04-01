import concurrent.futures
import json
import newspaper
import os
import sys

FEED_PATH = 'twitter_feeds'
ARTICLE_PATH = 'article_sources'


def get_article(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return {
        'url': article.url,
        'title': article.title,
        'authors': article.authors,
        'text': article.text,
    }


def save_source_articles(handle):
    tweet_filename = os.path.join(FEED_PATH, handle + '.json')
    if not os.path.isfile(tweet_filename):
        print('No Twitter feed for @' + handle)
        return
    article_filename = os.path.join(ARTICLE_PATH, handle + '.json')
    if os.path.isfile(article_filename):
        print('File ' + article_filename + ' already exists, skipping...')
        return

    print('Getting article sources for @' + handle + '...')
    with open(tweet_filename) as in_file:
        tweets = json.load(in_file)['tweets']
    articles_json = {}
    for tweet in tweets:
        for url_entity in tweet['entities']['urls']:
            url = url_entity['expanded_url']
            if url in articles_json:
                continue
            try:
                article = get_article(url)
                articles_json[url] = article
                sys.stdout.write('.')
                sys.stdout.flush()
            except:
                sys.stdout.write('!')
                sys.stdout.flush()
                continue

    print('Writing articles to file ' + article_filename + '...')
    with open(article_filename, 'w') as article_file:
        json.dump(articles_json, article_file, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    with open('sources.json') as sources_file:
        sources = json.load(sources_file)['sources']
    executor = concurrent.futures.ProcessPoolExecutor(10)
    for source in sources:
        for handle in source['twitter_handles']:
            executor.submit(save_source_articles, handle)
