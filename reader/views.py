from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Article, Category

def index(request):
    latest_article_list = Article.objects.order_by('headline')[:5]
    context = {
        'latest_article_list': latest_article_list,
    }
    return render(request, 'reader/index.html', context)

def categories(request, categoy_id):
    all_categories = Category.objectsorder_by('name')
    context = {
        'all_categories':all_categories,
    }
    return render(request, 'reader/categories.html', context)

def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'reader/article.html', {'article':article})
