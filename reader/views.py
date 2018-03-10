from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

#from .models import Article, Category, DictionaryEntry
from .models import Article, Category
from .models import Dictionary

import jieba
import collections
import pandas as pd

def index(request):
    latest_article_list = Article.objects.order_by('headline')[:100]
    context = {
        'latest_article_list': latest_article_list,
    }
    return render(request, 'reader/index.html', context)

def categories(request):
    all_categories = Category.objects.order_by('name')
    context = {
        'all_categories':all_categories,
    }
    return render(request, 'reader/categories.html', context)

def category(request, category_name):
    category = get_object_or_404(Category, pk=category_name)
    associated_articles = category.article_set.all()
    context = {
        'category':category,
        'associated_articles':associated_articles,
    }
    return render(request, 'reader/category.html', context)

def article_nopopover(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    d = Dictionary.d
    cedict = set(d['simplified'])
    segments = jieba.lcut(article.body)
    in_cedict = [s in cedict for s in segments]
    hl_segments = []
    for i in range(len(segments)):
        if in_cedict[i]:
            hl_segments.append('<a href="/reader/explain/{}">{}</a>'.format(segments[i],segments[i]))
        else:
            hl_segments.append(segments[i])

    context = {
        'article':article,
        'hlarticle':"".join(hl_segments),
        }
    return render(request, 'reader/article.html', context)

def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    d = Dictionary.d
    cedict = set(d['simplified'])
    segments = jieba.lcut(article.body)
    d = d[d['simplified'].isin(segments)]
    d = d.groupby('simplified').agg({'english':'\n'.join})
    segments = pd.DataFrame(segments, columns=['segment'])
    segments = segments.join(d, on='segment')
    segments = segments.fillna(False)
    segments_dicts = list(segments.T.to_dict().values())
    Segment=collections.namedtuple('Segment', 'segment english')
    segments = [Segment(s['segment'], s['english']) for s in segments_dicts]
    context = {
        'article':article,
        'segments':segments,
        }
    return render(request, 'reader/article_popover.html', context)

def explain(request, word):
    DictionaryEntry = collections.namedtuple('Entry', 'pinyin translation')
    d = Dictionary.d
    d = d[d['simplified'] == word]
    if d.empty:
        raise Http404
    de = d.apply(lambda r:DictionaryEntry(r['pinyin'], r['english']), axis=1)
    de = de.tolist()
    context = {
        'word':word,
        'entries':de,
        }
    return render(request, 'reader/explain.html', context)

def explain_dbdict(request, word):
    words = get_list_or_404(DictionaryEntry, word=word)
    context= {
        'word':word,
        'entries':words,
        }
    return render(request, 'reader/explain.html', context)

def bstest(request):
    return render(request, 'reader/bstest.html')
