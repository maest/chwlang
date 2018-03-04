from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.article, name='article'),
    path('categories/', views.categories, name='categories'),
    path('category/<category_name>/', views.category, name='category'),
    path('explain/<word>/', views.explain, name='explain'),
]
