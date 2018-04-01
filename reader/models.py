from django.db import models
from io import StringIO
import pandas as pd
import requests
import os
import uuid
from pathlib import Path

from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Article(models.Model):
    url = models.CharField(max_length=500, primary_key=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    headline = models.CharField(max_length=500)
    body = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('headline',)

def download_file_from_filesystem():
    filepath=Path(settings.BASE_DIR)/'data/cedict/dictionary_df.csv'
    print('Reading dictionary csv from disk')
    with open(str(filepath), 'r', encoding='utf-8') as f:
        r = f.read()
    print('Done reading dictionary csv from disk')
    return r

class Dictionary():
    csv_text = download_file_from_filesystem()
    d = pd.read_csv(StringIO(csv_text),
                    sep='\t',
                    encoding='utf-8')
