from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

#from .models import Article, Category, DictionaryEntry
from .models import Article, Category
from .models import Dictionary

import jieba
import collections

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

def article(request, article_id):
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

def article_dbdict(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    cedict = [e.word for e in DictionaryEntry.objects.only('word')]
    cedict = set(cedict)
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
