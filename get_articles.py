import concurrent.futures
import json
import newspaper
import os
import sys

FEED_PATH = 'twitter_feeds'
ARTICLE_PATH = 'article_sources'
RETRY_FAILED = True


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
    print()
    tweet_filename = os.path.join(FEED_PATH, handle + '.json')
    if not os.path.isfile(tweet_filename):
        print('No Twitter feed for @' + handle)
        return
    
    article_filename = os.path.join(ARTICLE_PATH, handle + '.json')
    if os.path.isfile(article_filename):
        if not RETRY_FAILED:
            print('File ' + article_filename + ' already exists, skipping...')
            return
        print('Retrying failed articles for @' + handle + '...')
        with open(article_filename, 'r') as article_file:
            articles_json = json.load(article_file)
    else:
        print('Getting article sources for @' + handle + '...')
        articles_json = {}

    
    with open(tweet_filename) as in_file:
        tweets = json.load(in_file)['tweets']
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

    print('\nWriting articles to file ' + article_filename + '...')
    with open(article_filename, 'w') as article_file:
        json.dump(articles_json, article_file, indent=2)


if __name__ == '__main__':
    with open('sources.json') as sources_file:
        sources = json.load(sources_file)['sources']
    executor = concurrent.futures.ProcessPoolExecutor(10)
    for source in sources:
        for handle in source['twitter_handles']:
            executor.submit(save_source_articles, handle)
