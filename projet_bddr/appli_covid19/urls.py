from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('theme/',views.themes, name='theme'),
    path('journaux/',views.journaux, name='journaux'),
    path('journaux2/',views.journaux2, name='journaux2'),
    path('journaux3/',views.journaux3, name='journaux3'),
    path('articles/',views.des_articles, name='articles'),
    path('articles2/',views.des_articles2, name='articles2'),
    path('histogram/',views.histogram, name='histogram'),
    path('histogram_annee/',views.histogram_annee, name='histogram_annee'),
    path('histogram_mois/',views.histogram_mois, name='histogram_mois'),
    path('histogram_semaine/',views.histogram_semaine, name='histogram_semaine'),
    path('histogram_date/',views.histogram_date, name='histogram_date'),
    path('affiliations/',views.affiliations, name='affiliations'),
    path('affiliations2/',views.affiliations2, name='affiliations2'),
    path('affiliations3/',views.affiliations3, name='affiliations3'),
    path('affiliations/<name_affiliation>',views.affiliation, name='affiliation'),
    path('theme/<name_theme>', views.sous_themes, name='<name_theme>'),
    path('articles/<name_article>',views.un_article, name='<name_article>'),
    path('sous_theme/<name_sous_theme>', views.articles, name='<name_sous_theme>'),
    path('journaux/<name_journal>', views.journal, name='<name_journal>'),
]
