import xml.etree.ElementTree
from pathlib import Path

from reader.models import Article, Category
import json

download_path = Path('C:/python projects/christina_website/chwlang/data/articles/downloads')

def run():
    for p in download_path.iterdir():
        with open(p, 'r', encoding='utf-8') as f:
            article_map = json.load(f)
        article = Article(headline = article_map['headline'],
                          body = article_map['body'])
        article.save()
        categories = [Category.objects.get_or_create(name = c)[0]
                      for c in article_map['categories']]
        for c in categories:
            article.categories.add(c)
        article.save()
