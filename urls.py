from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('themes',views.themes, name='themes'),
    #path('articles',views.articles, name='articles'),
    path('page',views.page, name='page'),
]
