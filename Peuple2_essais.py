import pandas as pd
import os
import json

"""
Création du metadata2 pour peupler les tables articles, article_theme et studytype_articles.
"""

chemin_archive ="/users/2023/ds1/share/CORD-19"
chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]

chemin1 = f'{chemin_archive}/document_parses/pmc_json'
elements1 = os.listdir(chemin1)

chemin2 = f'{chemin_archive}/document_parses/pdf_json'
elements2 = os.listdir(chemin2)

DF=pd.read_csv(f'{chemin_archive}/metadata.csv')
#############################################  LISTE DES STUDYTYPE POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
Articles=[]
Study_Article=[]
for dossier in dossiers[1:-1]:
    chemin = f'{chemin_tables}/{dossier}'
    elements = os.listdir(chemin)
    for element in elements :
        df=pd.read_csv(f'{chemin}/{element}')
        try :
            for i in range(len(df)):
                study_article=(df['Study Type'][i],df['Study'][i])
                Articles.append(df['Study'][i])
                Study_Article.append(study_article)
        except:
            print(f"Le fichier {chemin}/{element} n'a pas de studytype !")
	
Study_Articles2={}
for Article in set(Articles):
    types=[]
    for i in range(len(Study_Article)):
        if Study_Article[i][1]==Article:
            types.append(Study_Article[i][0])

Study_types=[]
for article_titre in DF['title']:
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
    Study_Articles2[Article]=list(set(types))
#############################################  LISTE DES SOUS_THEMES POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
Sous_themes_articles={}
for dossier in dossiers[1:-1]:
        chemin = f'{chemin_tables}/{dossier}'
        elements = os.listdir(chemin)
        for element in elements :
            sous_theme = f'{element[:-4]}'
            da= pd.read_csv(f'{chemin}/{element}')
            Sous_themes_articles[sous_theme]=da['Study'].str.upper().unique()

Sous_themes_articles2=[]
for article_title in DF['title']:
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
	
DF2=pd.DataFrame({'title' : DF['title'], 'abstract' : DF['abstract'], 'publish_time' : DF['publish_time'], 'journal' : DF['journal'], 
                  'url' : DF['url'], 'studytype' : Study_types, 'sous_themes' : Sous_themes_articles2})
#print(DF2[DF2['sous_themes']!='NULL'])
#DF2.to_csv("metadata2.csv")

"""
Création du metadata3 pour peupler les tables authors, author_affiliation et author_article.
"""
