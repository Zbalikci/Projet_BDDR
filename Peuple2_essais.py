from appli_covid19.models import Articles,Journal,StudyType_Articles,StudyType, Sous_Theme, Article_Theme
from django.db import IntegrityError
from datetime import datetime
import pandas as pd
import os
import json

"""
Création des listes pour peupler les tables articles, article_theme et studytype_articles.
"""

chemin_archive ="/users/2023/ds1/share/CORD-19"
chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]

chemin1 = f'{chemin_archive}/document_parses/pmc_json'
elements1 = os.listdir(chemin1)

chemin2 = f'{chemin_archive}/document_parses/pdf_json'
elements2 = os.listdir(chemin2)

print('chargement metadata')
DF=pd.read_csv(f'{chemin_archive}/metadata.csv')
print('chargement metadata fini')

#######################################
n=9000
#######################################

#############################################  LISTE DES STUDYTYPE POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
print('Liste Articles création : début')
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
print('Liste Articles création : fin')
print('Liste Study_Articles2 création : début')
Study_Articles2={}
for Article in set(Articles0):
    types=[]
    for i in range(len(Study_Article)):
        if Study_Article[i][1]==Article:
            types.append(Study_Article[i][0])
    Study_Articles2[Article]=list(set(types))
print('Liste Study_Articles2 création : fin')
print('Liste Study_types création : début')

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
        print(article_titre)
        print('OK')
    else:
        Study_types.append('NULL')

print('Liste Study_types création : fin')
#############################################  LISTE DES SOUS_THEMES POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
print('Liste Sous_themes création : début')
Sous_themes_articles={}
for dossier in dossiers[1:-1]:
        chemin = f'{chemin_tables}/{dossier}'
        elements = os.listdir(chemin)
        for element in elements :
            sous_theme = f'{element[:-4]}'
            da= pd.read_csv(f'{chemin}/{element}')
            Sous_themes_articles[sous_theme]=da['Study'].str.upper().unique()

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
# Remplissage table Arcticles
print('Debut peuplement')
for i in range(n):
    if type(DF['journal'][i])==float:
        id_journal=Journal.objects.get(name = 'NULL')
    else:
        id_journal = Journal.objects.get(name = DF['journal'][i])
    un_article = Articles()
    un_article.title = DF['title'][i]
    un_article.publish_time=str(DF['publish_time'][i])
    un_article.abstract = DF['abstract'][i]
    un_article.stulink = DF['url'][i]
    un_article.journal = id_journal
    un_article.save()

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

"""
Création du metadata3 pour peupler les tables authors, author_affiliation et author_article.
"""
import unidecode
#############################################  LISTE DES AUTEURS_PMC POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
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
#############################################  LISTE DES AUTEURS_PDF POUR CHAQUE ARTICLE DE METADATA.CSV  #############################################
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

DF4=pd.DataFrame({'Title': DF['title'][:100],'Authors': DF['authors'][:100],'Authors_files': Authors_files , 'Emails_files' : Emails_files, 
                  'Institution':Institution, 'Laboratory': Laboratory})

############################################## CREATION DU DATAFRAME 1 LIGNE = 1 AUTEUR #############################################
final_title=[]
final_author=[]
final_email=[]
final_inst=[]
final_labo=[]

for i in range(15):
    L=DF4['Authors_files'][i]
    s=DF4['Authors'][i]
    t=DF4['Title'][i]
    E=DF4['Emails_files'][i]
    INST=DF4['Institution'][i]
    LABO=DF4['Laboratory'][i]
    etat=False
    for l in L:
        index=L.index(l)
        l2=unidecode.unidecode("".join(list(filter(str.isalpha,l )))).upper()
        for k in s.split('; '): 
            k2=unidecode.unidecode("".join(list(filter(str.isalpha,k )))).upper()
            if (l2 in k2) or (k2 in l2):
                etat=True 
                K=k
                
        if etat:
            if K not in final_author: #si l'auteur se trouce >2 fois dans L
                final_author.append(K)
                final_email.append(E[index])
                final_title.append(t)
                if INST!=[]:
                    final_inst.append(INST[index])
                else:
                    final_inst.append('NULL')
                if LABO!=[]:
                    final_labo.append(LABO[index])
                else:
                    final_labo.append('NULL')
            else:
                index2=final_author.index(K)
                if E[index]==str and E[index]>3:
                    E[index2]=E[index]
        else:
            final_author.append(l)
            final_email.append(E[index])
            final_title.append(t)
            if INST!=[]:
                final_inst.append(INST[index])
            else:
                final_inst.append('NULL')
            if LABO!=[]:
                final_labo.append(LABO[index])
            else :
                final_labo.append('NULL')
		
DF5=pd.DataFrame({'Title': final_title,'Authors': final_author, 'Emails_files' : final_email, 
                  'Institution':final_inst, 'Laboratory': final_labo})
