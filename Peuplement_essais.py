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
print("Par exemple : 'D:/archive/Kaggle'   ou  'D:/archive/metadata.csv'")
print("Dans ce cas : chemin_archive = 'D:/archive' ")
chemin_archive = input("Veuillez donner le chemin : chemin_archive= ") or "D:/archive"

chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]
print("En train de charger le fichier metadata.csv")
df=pd.read_csv(f'{chemin_archive}/metadata.csv')
print("En train de récupérer la liste des journaux dans metadata.csv")
l=df["journal"][:100].unique()

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
    connection = psycopg2.connect("host=localhost dbname=covid19 user=postgres password=Zor.bulursun1")
    cursor = connection.cursor()
    print("Création d'individus NULL pour les tables theme, sous_theme, studytype et affiliation :")
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
        cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",('NULL','NULL','NULL'))
    print("Individu NULL pour les tables theme, sous_theme, studytype et affiliation a été crée")
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
        cursor.execute("""SELECT * FROM appli_covid19_journal WHERE name LIKE %s""", (l[i],))
        records = cursor.fetchall()
        if records==[]:
            cursor.execute("""INSERT INTO appli_covid19_journal(name) VALUES(%s);""",(l[i],))
    print('peuplement de la table journal : fin')

    chemin1 = f'{chemin_archive}/document_parses/pdf_json'
    elements1 = os.listdir(chemin1)
    #les auteurs dans le pmc_json semble ne pas avoir d'affiliation
    chemin2 = f'{chemin_archive}/document_parses/pmc_json'
    elements2 = os.listdir(chemin2)
    print('peuplement de la table affiliation : début')
    for element in elements1[:50]:
        with open(f'{chemin1}/{element}', 'r') as f:
            data = json.load(f)
        if len(data['metadata']['authors'])!=0:
            for i in range(len(data['metadata']['authors'])):
                l= data['metadata']['authors'][i]['affiliation']
                if l!={}:
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
                    L = l['location']
                    c=L.values()
                    k=[j for j in c]
                    location=" ".join(str(K).upper() for K in k)
                    if type(name) == list: 
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name[0],))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name[0],'laboratory'.upper(),location.upper()))
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name[1],))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name[1],'institution'.upper(),location.upper()))
                    else:
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name,))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name,typ.upper(),location.upper()))
    for element in elements2[:50]:
        with open(f'{chemin2}/{element}', 'r') as f:
            data = json.load(f)
        if len(data['metadata']['authors'])!=0:
            for i in range(len(data['metadata']['authors'])):
                l= data['metadata']['authors'][i]['affiliation']
                if l!={}:
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
                    L = l['location']
                    c=L.values()
                    k=[j for j in c]
                    location=" ".join(str(K).upper() for K in k)
                    if type(name) == list: 
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name[0],))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name[0],'laboratory'.upper(),location.upper()))
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name[1],))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name[1],'institution'.upper(),location.upper()))
                    else:
                        cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (name,))
                        records = cursor.fetchall()
                        if records==[]:
                            cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,location) VALUES(%s,%s,%s);""",(name,typ.upper(),location.upper()))
    print('peuplement de la table affiliation : fin')
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)

"""
#df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

#for i in range(100):
#	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')
"""
