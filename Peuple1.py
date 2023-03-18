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
l=df["journal"].unique()

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
    for element in elements1:
        with open(f'{chemin1}/{element}', 'r') as f:
            data = json.load(f)
            fichier+=1
            print("nombre de fichiers traités=",fichier)
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
                                cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name[0]),'laboratory'.upper(),country[:99].upper()))
                        if len(name[1])<799:

                            cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name[1]),))
                            records = cursor.fetchall()
                            if records==[]:
                                cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name[1]),'institution'.upper(),country[:99].upper()))
                    else:
                        if len(name)<799:

                            cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name),))
                            records = cursor.fetchall()
                            if records==[]:
                                cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name),typ.upper(),country[:99].upper()))

    print('peuplement de la table affiliation : fin')
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)
