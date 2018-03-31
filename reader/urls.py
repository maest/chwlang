from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='article_index'),
    path('nopopover/<uuid:article_id>/', views.article_nopopover, name='article_nopopver'),
    path('<uuid:article_id>/', views.article, name='article'),
    path('categories/', views.categories, name='categories'),
    path('category/<category_name>/', views.category, name='category'),
    path('explain/<word>/', views.explain, name='explain'),
    path('explain_popover/<word>/', views.explain_popover, name='explain_popover'),
    path('bstest', views.bstest, name='bstest'),
    path('base', views.base, name='base'),
]
