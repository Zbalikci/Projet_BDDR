#!/bin/env python3
import pandas as pd
import logging
import psycopg2
import os
import json
from django.db import models

"""
Pour peupler les tables theme, sous_theme et journal:
"""

chemin = "/users/2023/ds1/share/CORD-19/Kaggle/target_tables"
elements = os.listdir(chemin)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin, element))]
df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")
l=df["journal"][:100].unique()

try:
	connection = psycopg2.connect("host=data dbname=zbalikci user=zbalikci password=zbalikci")
	cursor = connection.cursor()
	for dossier in dossiers[1:-1]:
		theme=(dossier[2:].replace("_"," ")).upper()
		cursor.execute("""
		INSERT INTO appli_covid19_theme(name)
		VALUES(%s)
		RETURNING id;
		""",
		(theme,)) # IMPORTANT LORSQU'IL Y A UN SEUL VALEUR !!! RAJOUTER VIRGULE , !!!!
		id_theme=cursor.fetchone()[0]
		chemin = f'/users/2023/ds1/share/CORD-19/Kaggle/target_tables/{dossier}'
		elements = os.listdir(chemin)
		for element in elements :
			cursor.execute("""
			INSERT INTO  appli_covid19_sous_theme(name,theme_id)
			VALUES(%s,%s);
			""",
			(f'{element[:-4]}',id_theme))
			
	for i in range(len(l)):
		cursor.execute("""
		INSERT INTO appli_covid19_journal(name)
		VALUES(%s);
		""",
		(l[i],))
	connection.commit()
	connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)


"""
#df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

#for i in range(100):
#	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')





chemin1 = "D:/archive/document_parses/pdf_json"
chemin2 = "D:/archive/document_parses/pmc_json"

elements = os.listdir(chemin1)

try:
    connection = psycopg2.connect("host=localhost dbname=covid19 user=postgres password=Zor.bulursun1")
    cursor = connection.cursor()
    cursor.execute("""
	INSERT INTO appli_covid19_affiliation(name,type,location)
	VALUES(%s,%s,%s);
	""",
	('NULL','NULL','NULL'))
    for element in elements[:100]:
        # Ouvrir le fichier JSON
        with open(f'{chemin1}/{element}', 'r') as f:
            data = json.load(f)
        # Accéder aux données dans le fichier JSON
        if len(data['metadata']['authors'])!=0:
            for i in range(len(data['metadata']['authors'])):
                l= data['metadata']['authors'][i]['affiliation']
                if l!={}:
                    if l['institution'] != '':
                        name = l['institution']
                        type='institution'
                    else:
                        name = l['laboratory']
                        type='laboratory'
                    L = l['location']
                    c=L.values()
                    k=[j for j in c]
                    location=" ".join(str(K).upper() for K in k)
                cursor.execute("SELECT * FROM appli_covid19_affiliation")
                records = cursor.fetchall()
                for r in records:
                    if r[1]!=name:
                        cursor.execute("""
		            INSERT INTO appli_covid19_affiliation(name,type,location)
		            VALUES(%s,%s,%s);
		            """,
		            (name,type.upper(),location.upper())) 
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)


elements = os.listdir(chemin2)      #les auteurs dans le pmc_json semble ne pas avoir d'affiliation

try:
    connection = psycopg2.connect("host=localhost dbname=covid19 user=postgres password=Zor.bulursun1")
    cursor = connection.cursor()
    for element in elements[:100]:
        with open(f'{chemin2}/{element}', 'r') as f:
            data = json.load(f)
        if len(data['metadata']['authors'])!=0:
            for i in range(len(data['metadata']['authors'])):
                l= data['metadata']['authors'][i]['affiliation']
                if l!={}:
                    if l['institution'] != '':
                        name = l['institution']
                        type='institution'
                    else:
                        name = l['laboratory']
                        type='laboratory'
                    L = l['location']
                    c=L.values()
                    k=[j for j in c]
                    location=" ".join(str(K).upper() for K in k)
                cursor.execute("SELECT * FROM appli_covid19_affiliation")
                records = cursor.fetchall()
                for r in records:
                    if r[1]!=name:
                        cursor.execute("""
		            INSERT INTO appli_covid19_affiliation(name,type,location)
		            VALUES(%s,%s,%s);
		            """,
		            (name,type.upper(),location.upper())) 
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)
        
"""

