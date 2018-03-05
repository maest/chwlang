import xml.etree.ElementTree
from pathlib import Path

from reader.models import Article, Category
import json
import requests
import zipfile
import io

file_id = '1PiUCl4amn5w3rBdQb68-JJFV8iup9sWr'

def download_file_from_google_drive(id):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = False)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = False)
    file_bytes = next(response.iter_content(chunk_size=None))
    return file_bytes

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def run():
    print("Downloading zip")
    f = download_file_from_google_drive(file_id)
    print("Done downloading zip")
    zf = zipfile.ZipFile(io.BytesIO(f), "r")
    articles = []
    for fileinfo in zf.infolist()[1:]:
        a = zf.read(fileinfo).decode('utf-8')
        article_map = json.loads(a)
        article = Article(headline = article_map['headline'],
                          body = article_map['body'])
        article.save()
        categories = [Category.objects.get_or_create(name = c)[0]
                      for c in article_map['categories']]
        for c in categories:
            article.categories.add(c)
        if 0 == Article.objects.filter(headline=article_map['headline']).count():
            print('Saving article: {}'.format(article.headline))
            article.save()
        else:
            print('Skipped saving article: {}'.format(article.headline))
