from django.db import models
from io import StringIO
import pandas as pd
import requests

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

def download_file_from_google_drive(id):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    print("Downloading dictionary csv")
    response = session.get(URL, params = { 'id' : id }, stream = False)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = False)
    csv_text = list(response.iter_content(chunk_size=None))[0].decode('utf-8')
    print("Done downloading dictionary csv")
    return csv_text

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

class Dictionary():
    csv_text = download_file_from_google_drive('101dprpGjFCSoSLa3bhrMsZwx_bfPrXxW')
    d = pd.read_csv(StringIO(csv_text),
                    sep='\t',
                    encoding='utf-8')
