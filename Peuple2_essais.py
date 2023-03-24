"""
Pour peupler les tables authors, articles, articles_sous_themes, authors_articles et affiliation_authors
"""
df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

for i in range(100):
	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')


	
	

chemin_archive ="/users/2023/ds1/share/CORD-19"
chemin1 = f'{chemin_archive}/document_parses/pmc_json'
elements1 = os.listdir(chemin1)

""" Construction de la liste des auteurs sous forme d'un dictionnaire dans les fichiers pmc_json """
fichier=0
print("En train de charger le fichier metadata.csv")
df=pd.read_csv(f'{chemin_archive}/metadata.csv')
Authors={}
for authors in df['authors'][:50]:
    try :
        for author in authors.split(';'):
            if author.startswith(' '):
                a=author[1:]
                Authors[a]=''
            else:
                Authors[author]=''
    except:
        Authors[authors]=''

for element in elements1[:100]:
    with open(f'{chemin1}/{element}', 'r') as f:
        data = json.load(f)
        fichier+=1
        print("nombre de fichiers dans pmc_json traités=",fichier)
        a=data['metadata']['authors']
    if len(a)!=0:
        for i in range(len(a)):
            first="".join(list(filter(str.isalpha,a[i]['first'] )))
            last="".join(list(filter(str.isalpha,a[i]['last'])))
            email= a[i]['email']
            if first=='' or first==' ':
                name_author = last
            if last=='' or last==' ':
                name_author=first
            else:
                name_author=last+', '+first
        Authors[name_author]=email
for i in Authors.keys():
    print(i,' = ',Authors[i])


	
	
"""
VERIFIER LES BOUCLES IF :
"""

#!/bin/env python3
import pandas as pd
import logging
import psycopg2
import os
import json
from django.db import models

"""
Pour peupler les tables theme, sous_theme, studytype, affiliation et journal:
"""
print("Où se trouve vos fichiers/dossiers Kaggle, documents_parses et metadata.csv ?")
chemin_archive = input("Veuillez donner le chemin : chemin_archive=") or "D:/archive"
host=input("HOST=") or "localhost"
dbname=input("DB_NAME=") or "covid19"
user=input("USER_NAME=") or "postgres"
password=input("PASSWORD=") or "Zor.bulursun1"

chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]
print("En train de charger le fichier metadata.csv")
df=pd.read_csv(f'{chemin_archive}/metadata.csv')
print("En train de récupérer la liste des journaux dans metadata.csv")
l=df["journal"].unique()[:100]

print("En train de crée la liste pour peupler la table studytype")

liste=[]
for dossier in dossiers[1:-1]:
	chemin = f'{chemin_tables}/{dossier}'
	elements = os.listdir(chemin)
	for element in elements :
		df=pd.read_csv(f'{chemin}/{element}')
		try :
			types=df['Study Type'].unique()
			for t in types:
				liste.append(t)
		except:
			pass
liste=list(set(liste))  

print("\nESSAI PEUPLEMENT DEBUT\n")

try:
    connection = psycopg2.connect(f'host={host} dbname={dbname} user={user} password={password}')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM appli_covid19_theme WHERE name LIKE %s""", ('NULL',))
    records = cursor.fetchall()
    if records==[]:
        cursor.execute("""INSERT INTO appli_covid19_theme(name) VALUES(%s) RETURNING id;""",('NULL',)) 
        id_theme=cursor.fetchone()[0]
    else :
        id_theme=records[0][1]
    cursor.execute("""SELECT * FROM appli_covid19_sous_theme WHERE name LIKE %s""", ('NULL',))
    records = cursor.fetchall()
    if records==[]:
        cursor.execute("""INSERT INTO appli_covid19_sous_theme(name,theme_id) VALUES(%s,%s);""",('NULL',id_theme))

    cursor.execute("""SELECT * FROM appli_covid19_studytype WHERE name LIKE %s""", ('NULL',))
    records = cursor.fetchall()
    if records==[]:
        cursor.execute("""INSERT INTO appli_covid19_studytype(name) VALUES(%s);""",('NULL',))
	
    cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", ('NULL',))
    records = cursor.fetchall()
    if records==[]:
        cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",('NULL','NULL','NULL'))
    print('peuplement des tables themes et sous_themes : début')
    for dossier in dossiers[1:-1]:
        theme=(dossier[2:].replace("_"," ")).upper()

        cursor.execute("""SELECT * FROM appli_covid19_theme WHERE name LIKE %s""", (theme,))
        records = cursor.fetchall()
        if records==[]:
            cursor.execute("""INSERT INTO appli_covid19_theme(name) VALUES(%s) RETURNING id;""",(theme,)) 
            id_theme=cursor.fetchone()[0]
        else:
            id_theme=records[0][1]
        chemin = f'{chemin_tables}/{dossier}'
        elements = os.listdir(chemin)
        for element in elements :
            cursor.execute("""SELECT * FROM appli_covid19_sous_theme WHERE name LIKE %s""", (f'{element[:-4]}',))
            records = cursor.fetchall()
            if records==[]:
                cursor.execute("""INSERT INTO  appli_covid19_sous_theme(name,theme_id) VALUES(%s,%s);""",(f'{element[:-4]}',id_theme))
    print('peuplement des tables themes et sous_themes : fin')
    print('peuplement de la table studytype : début')
    for study in liste:
        cursor.execute("""SELECT * FROM appli_covid19_studytype WHERE name LIKE %s""", (str(study),))
        records = cursor.fetchall()
        if records==[]:
            cursor.execute("""INSERT INTO appli_covid19_studytype(name) VALUES(%s);""",(str(study),))
    print('peuplement de la table studytype : fin')
    print('peuplement de la table journal : début')
    for i in range(len(l)):
        cursor.execute("""SELECT * FROM appli_covid19_journal WHERE name LIKE %s""", (str(l[i]),))
        records = cursor.fetchall()
        if records==[]:
            cursor.execute("""INSERT INTO appli_covid19_journal(name) VALUES(%s);""",(str(l[i]),))
    print('peuplement de la table journal : fin')

    chemin1 = f'{chemin_archive}/document_parses/pdf_json'
    elements1 = os.listdir(chemin1)
    #les auteurs dans le dossier pmc_json n'ont pas d'affiliation

    print('peuplement de la table affiliation : début')
    fichier=0
    for element in elements1[:100]:
        with open(f'{chemin1}/{element}', 'r') as f:
            data = json.load(f)
            fichier+=1
            print("nombre de fichiers traités=",fichier)
            a=data['metadata']['authors']

        if len(a)!=0:
            for i in range(len(a)):
                first="".join(list(filter(str.isalpha,a[i]['first'] )))
                if len(a[i]['middle'])<=1:
                    m="".join(a[i]['middle'])
                else :
                    m=" ".join(a[i]['middle'])
                middle="".join(list(filter(str.isalpha,m )))
                suffix="".join(list(filter(str.isalpha,a[i]['suffix'] )))
                last="".join(list(filter(str.isalpha,a[i]['last'] )))
                email= a[i]['email']
                if first=='':
                    if middle=='' and suffix=='':
                        name_author = last
                    else:
                        name_author=last+', '+middle+suffix
                if last=='':
                    name_author=first+' '+middle+suffix
                else:
                    name_author=last+', '+first+' '+middle+suffix

                l= a[i]['affiliation']
                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", ('NULL',))
                id_affiliation_null =cursor.fetchone()[0]

                cursor.execute("""SELECT * FROM appli_covid19_authors WHERE name LIKE %s""", (str(name_author),))
                records = cursor.fetchall()
                if records==[]:
                    cursor.execute("""INSERT INTO appli_covid19_authors(name,email) VALUES(%s,%s) RETURNING id;""",(str(name_author),email))
                    id_author =cursor.fetchone()[0]
                    if l=={}:
                        cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation_null,id_author))
                    else:
                        if l['institution'] == '':
                            name = l['laboratory']
                            typ='laboratory'
                        elif l['laboratory']== '':
                            name = l['institution']
                            typ='institution'
                        else:
                            name=[]
                            name.append(l['laboratory'])
                            name.append(l['institution'])
                        if element=='019dd2d404fefff0604e0dff0d114adf358f341d.json':
                            name='University of Vermont Medical Center'
                            typ='institution'
                            country='Vermont, USA'
                        
                        if l['location']!={} and ('country' in l['location']) :
                            country = l['location']['country']
                        else:
                            country='NULL'
                        if element=='11ec74432d6eeeb47e9f7d6947c9ca2bb2ce805f.json':
                            country='California, USA'
                        if element=='00624a8e79f31fccd9cc02ac643e8481d78898af.json' and i==9:
                            country='United States, Colombia'
                        if element=='016000d0032521cc2bc55a82ad6a17d1a5fa0d9c.json' and i==0:
                            country='The Netherlands'
                        if element=='023a4e1c632ed6a19085298853a7bd88277748fd.json' and i==12:
                            name='Biological Research Laboratory, Goiano Federal Institution -Urutaí Campus'
                        if element=='04da3272305af0fae4d2f18e1ba1ac22158003dd.json' and i==4:
                            country='UK, Germany, Italy, Netherlands, Spain, USA'
                        if element=='2468cfede566513e89672dbdd4a6ea5d236990cd.json' and (i==6 or i ==8):
                            typ='institution'
                            name='Ulster University'
                            country='Northern Ireland'
                        
                        if type(name) == list: 
                            if len(name[0])<799:

                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name[0]),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s) RETURNING id;""",(str(name[0]),'laboratory'.upper(),country[:99].upper()))
                                    id_affiliation1 =cursor.fetchone()[0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation1,id_author))
                                else:
                                    id_affiliation1=records[0][0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation1,id_author))
                            if len(name[1])<799:

                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name[1]),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s) RETURNING id;""",(str(name[1]),'institution'.upper(),country[:99].upper()))
                                    id_affiliation2 =cursor.fetchone()[0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation2,id_author))
                                else:
                                    id_affiliation2=records[0][0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation2,id_author))
                        else:
                            if len(name)<799:

                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s) RETURNING id;""",(str(name),typ.upper(),country[:99].upper()))
                                    id_affiliation =cursor.fetchone()[0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation,id_author))
                                else:
                                    id_affiliation=records[0][0]
                                    cursor.execute("""INSERT INTO appli_covid19_author_affiliation(affiliation_id,author_id) VALUES(%s,%s) ;""",(id_affiliation,id_author))


    print('peuplement de la table affiliation : fin')
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)
