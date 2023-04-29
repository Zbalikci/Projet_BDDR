from django.urls import path, re_path
from . import views
from appli_covid19.views import ArticleChart


urlpatterns = [
    path('', views.index, name='index'),
    path('theme/',views.themes, name='theme'),
    path('journaux/',views.journaux, name='journaux'),
    path('journaux2/',views.journaux2, name='journaux2'),
    path('articles/',views.des_articles, name='articles'),
    path('histogram/',views.histogram, name='histogram'),
    path('histogram_annee/',views.histogram_annee, name='histogram_annee'),
    path('histogram_mois/',views.histogram_mois, name='histogram_mois'),
    path('histogram_semaine/',views.histogram_semaine, name='histogram_semaine'),
    path('histogram_date/',views.histogram_date, name='histogram_date'),
    path('affiliations/',views.affiliations, name='affiliations'),
    path('affiliations2/',views.affiliations2, name='affiliations2'),
    path('affiliations/<name_affiliation>',views.affiliation, name='affiliation'),
    path('theme/<name_theme>', views.sous_themes, name='<name_theme>'),
    path('sous_theme/<name_sous_theme>', views.articles, name='<name_sous_theme>'),
    path('journaux/<name_journal>', views.journal, name='<name_journal>'),
    path('article_chart',ArticleChart.as_view(), name='article_chart'),
]
