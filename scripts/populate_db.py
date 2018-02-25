import xml.etree.ElementTree
from pathlib import Path

from reader.models import Article, Category

def run():
    category = Category(name='Finance')
    category.save()
    article_path = Path('C:/python projects/christina_website/chwlang/scripts/article1.txt')
    e = xml.etree.ElementTree.parse(article_path).getroot()
    article = Article(headline=e[0].text, body=e[1].text)
    article.save()
    article.categories.add(category)

    article_path = Path('C:/python projects/christina_website/chwlang/scripts/article2.txt')
    e = xml.etree.ElementTree.parse(article_path).getroot()
    article = Article(headline=e[0].text, body=e[1].text)
    article.save()
    article.categories.add(category)
