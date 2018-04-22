import logging
import pandas as pd
import numpy as np
import newspaper
import concurrent.futures
from reader.models import Article, Category
from django.utils.timezone import make_aware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_and_parse(article):
    article.download()
    article.parse()

def run():
    articles = Article.objects.all()
    urls = [(a.url, a.id) for a in articles]
    df = pd.DataFrame(urls, columns=['url', 'id'])
    df['n_article'] = df['url'].apply(lambda x:newspaper.Article(x, language='zh'))
    
    #parallel download an parse
    logger.info('Downloading {} articles'.format(len(df)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_date = {executor.submit(download_and_parse,
                                         article): idx
                         for idx, article in enumerate(df['n_article'])}
        for future in concurrent.futures.as_completed(future_to_date):
            idx = future_to_date[future]
            try:
                future.result()
            except Exception as exc:
                logger.error('%r generated an exception: %s' % (idx, exc))
    
    df['publish_date'] = df['n_article'].apply(lambda x:x.publish_date)
    df = df[~df['publish_date'].isnull()]
    df['publish_date'] = df['publish_date'].apply(make_aware)
    
    logger.info('Saving {} articles'.format(len(df)))
    for i, r in df.iterrows():
        a = Article.objects.get(id=r['id'])
        a.publish_date = r['publish_date']
        a.save()
    logger.info('Done saving {} articles'.format(len(df)))
