from django.urls import path
from . import views
from appli_covid19.views import ArticleChart


urlpatterns = [
    path('', views.index, name='index'),
    path('themes',views.themes, name='themes'),
    path('article_chart',ArticleChart.as_view(), name='article_chart'),
    
    

    #path('articles',views.articles, name='articles'),
]
