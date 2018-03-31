import newspaper
import pandas as pd
import logging
import sqlite3
import concurrent.futures
from pathlib import Path
from reader.models import Article, Category

from django.conf import settings

import logging
logger = logging.getLogger(__name__)

def build_xinhuanet_articles():
    url = 'http://www.xinhuanet.com'
    logger.info('Reading {}'.format(url))
    paper = newspaper.build(url, language='zh', memoize_articles=False)
    logger.info('Done building {}'.format(url))
    articles = pd.DataFrame(paper.articles, columns=['article'])
    source_filter_path = Path(settings.BASE_DIR)/'data/sources/xinhuanet.csv'
    cats = pd.read_csv(str(source_filter_path), index_col=False)
    cats = cats[cats['include']]
    articles['categories'] = articles['article'].apply(lambda x:match_category(x.url, cats))
    articles['url'] = articles['article'].apply(lambda x:x.url)
    articles = articles[articles['categories'].notnull()]
    articles['categories'] = articles['categories'].apply(lambda x:['xinhuanet',x])
    return articles

def build_163_articles():
    url = 'http://163.com'
    logger.info('Reading {}'.format(url))
    paper = newspaper.build(url, language='zh', memoize_articles=False)
    logger.info('Done building {}'.format(url))
    articles = pd.DataFrame(paper.articles, columns=['article'])
    source_filter_path = Path(settings.BASE_DIR)/'data/sources/163.csv'
    cats = pd.read_csv(str(source_filter_path), index_col=False)
    cats = cats[cats['include']]
    articles['categories'] = articles['article'].apply(lambda x:match_category(x.url, cats))
    articles['url'] = articles['article'].apply(lambda x:x.url)
    articles = articles[articles['categories'].notnull()]
    import pdb;pdb.set_trace()
    articles['categories'] = articles['categories'].apply(lambda x:['xinhuanet',x.split('/')[-1]])
    return articles

def download_and_parse_articles(articles):
    '''Returns a dataframe with columns url, categories, title, text
    '''
    articles = download_and_parse_articles_multiprocess(articles)
    articles['text'] = articles['article'].apply(lambda x:x.text)
    articles['title'] = articles['article'].apply(lambda x:x.title)
    articles = articles[['url','categories','title','text']]
    return articles

def download_and_parse_articles_multiprocess(articles):
    logger.info('Downloading {} articles'.format(len(articles)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_and_parse_article_single,
                                         a.article): idx
                         for idx, (_, a) in enumerate(articles.iterrows())}
        results = []
        for future in concurrent.futures.as_completed(future_to_url):
            idx = future_to_url[future]
            try:
                article = future.result()
            except Exception as exc:
                logger.error('%r generated an exception: %s' % (idx, exc))
    return articles

def download_and_parse_articles_singlethread(articles):
    logger.info('Downloading {} articles'.format(len(articles)))
    for idx,a in enumerate(articles['article']):
        logger.info('Doing {} out of {} articles'.format(1+idx, len(articles)))
        download_and_parse_article_single(a)
    logger.info('Done downloading articles')
    return articles

def download_and_parse_article_single(article): 
    logger.info('Downloading {}'.format(article.url))
    article.download()
    logger.info('Parsing {}'.format(article.url))
    article.parse()
    return article

def match_category(url, categories):
    for i, c in categories.iterrows():
       if url.startswith(c['url']):
           return c['category']
    return None

def save_full_articles_to_db(full_articles):
    '''full_articles is a dataframe with columns title, text, url, categories
    '''
    for i, a in full_articles.iterrows():
        new_a = Article(headline = a['title'],
                        body = a['text'],
                        url = a['url'])
        #save before adding categories, otherwise add fails
        new_a.save()
        cats = [Category.objects.get_or_create(name = c)[0] for c in a['categories']]
        new_a.categories.add(*cats)
        new_a.save()
