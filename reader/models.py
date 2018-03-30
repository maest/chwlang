from django.db import models
from io import StringIO
import pandas as pd
import requests
import os

class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Article(models.Model):
    headline = models.CharField(max_length=500)
    body = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('headline',)

#class DictionaryEntry(models.Model):
#    word = models.CharField(max_length=40)
#    pinyin = models.CharField(max_length=200)
#    translation = models.CharField(max_length=800)
#
#    def __str__(self):
#        return self.word
#
#    class Meta:
#        ordering = ('word',)

def get_filelink(file_id):
    from bs4 import BeautifulSoup
    response = requests.get('http://s000.tinyupload.com/?file_id=' + file_id)
    soup = BeautifulSoup(response.text, 'html.parser')
    for x in soup.find_all('a'):
        if x['href'].startswith('download.php'):
            full_link = 'http://s000.tinyupload.com/' + x['href']
            return full_link

def download_file_from_tinyupload(file_id):
    import time
    session = requests.Session()
    print("Downloading dictionary csv (Tinyupload)")
    t0 = time.time()
    file_link = get_filelink(file_id)
    response = session.get(file_link, stream = False)
    t1 = time.time()
    print(t1-t0)
    print('Getting confirm token')
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = False)
    csv_text = list(response.iter_content(chunk_size=None))[0].decode('utf-8')
    print("Done downloading dictionary csv")
    return csv_text

def download_file_from_google_drive(id):
    import time
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    print("Downloading dictionary csv")
    t0 = time.time()
    response = session.get(URL, params = { 'id' : id }, stream = False)
    t1 = time.time()
    print(t1-t0)
    print('Getting confirm token')
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = False)
    csv_text = list(response.iter_content(chunk_size=None))[0].decode('utf-8')
    print("Done downloading dictionary csv")
    return csv_text

def download_file_from_filesystem():
    filepath='/home/bogdan/projects/chwlang/chwlang/data/cedict/dictionary_df.csv'
    print('Reading dictionary csv from disk')
    with open(filepath, 'r', encoding='utf-8') as f:
        r = f.read()
    print('Done reading dictionary csv from disk')
    return r

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

class Dictionary():
    if 'YOU_ARE_ON_HEROKU' in os.environ:
        csv_text = download_file_from_google_drive('101dprpGjFCSoSLa3bhrMsZwx_bfPrXxW')
        #csv_text = download_file_from_tinyupload('87655706384298476180')
    else:
        csv_text = download_file_from_filesystem()
    d = pd.read_csv(StringIO(csv_text),
                    sep='\t',
                    encoding='utf-8')
