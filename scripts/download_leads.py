import xml.etree.ElementTree
from pathlib import Path

from reader.models import Article, Category

import newspaper
from newspaper import Article

import pandas as pd
import json

download_path = Path('C:/python projects/christina_website/chwlang/data/articles/downloads')
download_targets = Path('C:/python projects/christina_website/chwlang/data/articles/ML Product Content Leads CH v0.0.csv')

def run():
    targets = pd.read_csv(download_targets, skiprows=2)
    targets = targets.drop('Unnamed: 0', axis=1)
    targets = targets[['URL', 'Categories']]
    for idx, target in targets.iterrows():
        print("Doing {}".format(target['URL']))
        article = Article(target['URL'], language='zh')
        print('Download...')
        article.download()
        print('Parsing...')
        article.parse()
        print('Done parsing.')
        article_json = article_to_json(article, target['Categories'])
        save_path = download_path / article.title
        with open(save_path, 'w', encoding='utf-8') as f:
            print("Saving under {}".format(save_path))
            f.write(article_json)

def article_to_json(article, categories):
    m = {}
    m['headline'] = article.title
    m['body'] = article.text
    m['categories'] = categories.split('|')
    r = json.dumps(m)
    return r
