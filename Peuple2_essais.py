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
import unidecode

Authors_pmc=[] 
Emails1=[]
for k in range(100):
    file_pmc=DF['pmc_json_files'][k]
    auteurs=[]
    emails=[]
    if type(file_pmc) == str:
        with open(f'{chemin_archive}/{file_pmc}','r') as f:
            data=json.load(f)
            L=data['metadata']['authors']
            if len(L)!=0:
                for i in range(len(L)):
                    first="".join(list(filter(str.isalpha,L[i]['first'] )))
                    last="".join(list(filter(str.isalpha,L[i]['last'])))
                    name=unidecode.unidecode(last)+', '+unidecode.unidecode(first)
                    email=L[i]['email']
                    auteurs.append(name)
                    emails.append(email)
    Authors_pmc.append(auteurs)
    Emails1.append(emails)
	
Authors_pdf=[]
Emails2=[]
Laboratory=[]
Institution=[]
for k in range(100):
    auteurs_pdf=[]
    emails2=[]
    laboratory=[]
    institution=[]
    file_pdf=DF['pdf_json_files'][k]
    if type(file_pdf)==str:
############################### >2 PDF_JSON ###############################
# on n'a pas les même auteurs dans les >2 pdf 
        if ';' in file_pdf:
            liste_file=file_pdf.split(';')
            for fil in liste_file:
                if fil.startswith(' '):
                    try:
                        with open(f'{chemin_archive}/{fil[1:]}','r') as f:
                            data=json.load(f)
                            L=data['metadata']['authors']
                            if len(L)!=0:
                                for i in range(len(L)):
                                    first="".join(list(filter(str.isalpha,L[i]['first'] )))
                                    last="".join(list(filter(str.isalpha,L[i]['last'])))
                                    name=unidecode.unidecode(last)+', '+unidecode.unidecode(first)
                                    email=L[i]['email']
                                    if L[i]['affiliation']!={} :
                                        name_labo = unidecode.unidecode(L[i]['affiliation']['laboratory'])
                                        name_inst = unidecode.unidecode(L[i]['affiliation']['institution'])
                                    else :
                                        name_labo = 'NULL'
                                        name_inst = 'NULL'
                                    if name not in auteurs_pdf:
                                        auteurs_pdf.append(name)
                                        emails2.append(email)
                                        laboratory.append(name_labo)
                                        institution.append(name_inst)
                    except:
                        pass
                else:
                    try:
                        with open(f'{chemin_archive}/{fil}','r') as f:
                            data=json.load(f)
                            L=data['metadata']['authors']
                            if len(L)!=0:
                                for i in range(len(L)):
                                    first="".join(list(filter(str.isalpha,L[i]['first'] )))
                                    last="".join(list(filter(str.isalpha,L[i]['last'])))
                                    name=unidecode.unidecode(last)+', '+unidecode.unidecode(first)
                                    email=L[i]['email']
                                    if L[i]['affiliation']!={} :
                                        name_labo = unidecode.unidecode(L[i]['affiliation']['laboratory'])
                                        name_inst = unidecode.unidecode(L[i]['affiliation']['institution'])
                                    else :
                                        name_labo = 'NULL'
                                        name_inst = 'NULL'
                                    if name not in auteurs_pdf:
                                        auteurs_pdf.append(name)
                                        emails2.append(email)
                                        laboratory.append(name_labo)
                                        institution.append(name_inst)
                    except:
                        pass               
############################### 1 PDF_JSON ###############################
        else:
            try:
                with open(f'{chemin_archive}/{file_pdf}','r') as f:
                    data=json.load(f)
                    L=data['metadata']['authors']
                    if len(L)!=0:
                        for i in range(len(L)):
                            first="".join(list(filter(str.isalpha,L[i]['first'] )))
                            last="".join(list(filter(str.isalpha,L[i]['last'])))
                            name=unidecode.unidecode(last)+', '+unidecode.unidecode(first)
                            email=L[i]['email']
                            if L[i]['affiliation']!={} :
                                name_labo = unidecode.unidecode(L[i]['affiliation']['laboratory'])
                                name_inst = unidecode.unidecode(L[i]['affiliation']['institution'])
                            else :
                                name_labo = 'NULL'
                                name_inst = 'NULL'
                            auteurs_pdf.append(name)
                            emails2.append(email)
                            laboratory.append(name_labo)
                            institution.append(name_inst)
            except:
                pass
    Authors_pdf.append(auteurs_pdf)
    Emails2.append(emails2)
    Laboratory.append(laboratory)
    Institution.append(institution)
	
######################################## METTRE EN COMMUN LES AUTEURS DANS PMC ET PDF POUR LE MÊME ARTICLE ###############################

Authors_files=[]
Emails_files=[]
for k in range(len(Authors_pmc)):
    if Authors_pmc[k]==[] and Authors_pdf[k]!=[]:
        Authors_files.append(Authors_pdf[k])
        Emails_files.append(Emails2[k])
    elif Authors_pmc[k]!=[] and Authors_pdf[k]==[]:
        Authors_files.append(Authors_pmc[k])
        Emails_files.append(Emails1[k])
    elif Authors_pmc[k]==[] and Authors_pdf[k]==[]:
        Authors_files.append(Authors_pmc[k])
        Emails_files.append(Emails1[k])
    else:
        for j in range(len(Authors_pmc[k])):
            if Authors_pmc[k][j] not in Authors_pdf[k]:
                Authors_pdf[k].append(Authors_pmc[k][j])
                Emails2[k].append(Emails1[k][j])
                Institution[k].append('NULL')
                Laboratory[k].append('NULL')
            else:
                if type(Emails1[k][j])==str and len(Emails1[k][j])>2:  #on privéligie les emails dans les fichiers pmc car ils semblent être en "meilleur état"
                    index=Authors_pdf[k].index(Authors_pmc[k][j])
                    Emails2[k][index]=Emails1[k][j]
        Authors_files.append(Authors_pdf[k])
        Emails_files.append(Emails2[k])
print(len(Authors_files))
print(len(Emails_files))
