from appli_covid19.models import Theme, Sous_Theme, Journal, StudyType, Affiliation, Authors, Articles, Author_Article, Article_Theme, Author_Affiliation, StudyType_Articles
from django.db import IntegrityError
import pandas as pd
import os
import json
import unidecode
"""
Création des listes pour peupler les tables articles, article_theme et studytype_articles.
"""
print("Où se trouve vos fichiers/dossiers Kaggle, documents_parses et metadata.csv ?")
chemin_archive = input("Veuillez donner le chemin : chemin_archive (/users/2023/ds1/share/CORD-19)=") or "/users/2023/ds1/share/CORD-19"
n=input("Quelle est la taille de l'échantillon que vous voulez lancer ? (max=1056660)  =")
chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]

print('Chargement du fichier metadata.csv')
DF=pd.read_csv(f'{chemin_archive}/metadata.csv')
print('Chargement du fichier metadata.csv fini')

#############################################  LISTE DES STUDYTYPE POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
print('Liste Study_types création : début')
'''
Crétion d'une liste de tuples : [ (son_studytype, un_article) ,  (...,...)  ,  ... ]
'''
Articles0=[]
Study_Article=[]
for dossier in dossiers[1:-1]:
    chemin = f'{chemin_tables}/{dossier}'
    elements = os.listdir(chemin)
    for element in elements :
        df=pd.read_csv(f'{chemin}/{element}')
        try :
            for i in range(len(df)):
                study_article=(df['Study Type'][i],df['Study'][i])
                Articles0.append(df['Study'][i])
                Study_Article.append(study_article)
        except:
            print(f"Le fichier {chemin}/{element} n'a pas de studytype !")
''' 
Création d'un dictionnaire tel que : { un_artcile = [ liste de ses studytype] , ...}
'''
Study_Articles2={}
for Article in set(Articles0):
    types=[]
    for i in range(len(Study_Article)):
        if Study_Article[i][1]==Article:
            types.append(Study_Article[i][0])
    Study_Articles2[Article]=list(set(types))
'''
Création d'une liste telle que : pour chaque article/ligne du metadata.csv, on a la liste de ses studytypes
'''
Study_types=[]
for article_titre in DF['title'][:n]:
    etat=False
    for key in Study_Articles2:
        try :
            k=key.upper()
            a=article_titre.upper()
        except:
            k=key
            a=article_titre
        if a==k:
            cle=key
            etat=True
    if etat:
        Study_types.append(Study_Articles2[cle])
    else:
        Study_types.append('NULL')

print('Liste Study_types création : fin')
#############################################  LISTE DES SOUS_THEMES POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
print('Liste Sous_themes création : début')
''' 
Création d'un dictionnaire tel que : { un_sous_theme = [ liste des artciles de ce sous_themes] , ...}
'''
Sous_themes_articles={}
for dossier in dossiers[1:-1]:
        chemin = f'{chemin_tables}/{dossier}'
        elements = os.listdir(chemin)
        for element in elements :
            sous_theme = f'{element[:-4]}'
            da= pd.read_csv(f'{chemin}/{element}')
            Sous_themes_articles[sous_theme]=da['Study'].str.upper().unique()
'''
Création d'une liste telle que : pour chaque article/ligne du metadata.csv, on a ses sous_themes
'''
Sous_themes_articles2=[]
for article_title in DF['title'][:n]:
    k=[]
    for key in Sous_themes_articles:
        try:
            a=article_title.upper()
        except:
            a=article_title
        if a in Sous_themes_articles[key]:
            k.append(key)
    if len(k)!=0:
        Sous_themes_articles2.append(k)
    else:
        Sous_themes_articles2.append('NULL')
print('Liste Sous_themes création : fin')
#############################################  PEUPLEMENT DES 3 TABLES  #############################################
print('Debut peuplement')
for i in range(n):
    s=DF['journal'][i]
    if ("\\" in r"%r" % f"{s}" ):
        jo=unidecode.unidecode("".join(list(filter(str.isalpha,f"{s}"))))
    elif type(s)==float:
        jo='NULL'
    else:
        jo=s
    if i%100==0:
    	print(f"Ligne {i}")
    try:
        id_journal = Journal.objects.get(name = jo)
        un_article = Articles()
        un_article.title = DF['title'][i]
        un_article.publish_time=str(DF['publish_time'][i])
        un_article.abstract = DF['abstract'][i]
        un_article.stulink = DF['url'][i]
        un_article.journal = id_journal
        un_article.save()
    except:
        print("probleme à la ligne ", i)
    ############################################
    STA=StudyType_Articles()
    liste_studytype = Study_types[i]
    try:
        if type(liste_studytype)==list:
            print(liste_studytype)
            for k in range(len(liste_studytype)):
                id_studytype=StudyType.objects.get(name = str(liste_studytype[k]))
                STA.studytype=id_studytype
                STA.article=un_article
                STA.save()
        else:
            id_studytype=StudyType.objects.get(name = 'NULL')
            STA.studytype=id_studytype
            STA.article=un_article
            STA.save()
    except:
        print(Study_types[i])
    ############################################
    AT=Article_Theme()
    liste_sousthemes = Sous_themes_articles2[i]
    try:
        if type(liste_sousthemes)==list:
            print(liste_sousthemes)
            for k in range(len(liste_sousthemes)):
                id_sous_theme=Sous_Theme.objects.get(name = str(liste_sousthemes[k]))
                AT.sous_theme=id_sous_theme
                AT.article=un_article
                AT.save()
        else:
            id_sous_theme=Sous_Theme.objects.get(name = 'NULL')
            AT.sous_theme=id_sous_theme
            AT.article=un_article
            AT.save()
    except:
        print(Sous_themes_articles2[i])
