#!/bin/env python3
import pandas as pd
import logging
import psycopg2
import os
import json
from django.db import models
#from appli_covid19.models import Theme, Sous_Theme 

"""
Pour peupler les tables themes et sujets :
"""

connection = psycopg2.connect("host=data dbname=zbalikci user=zbalikci password=zbalikci")
cursor = connection.cursor()
sql="""
DROP TABLE IF EXISTS Theme;
CREATE TABLE Theme
  ( 
    id_theme     SERIAL PRIMARY KEY NOT NULL, 
    theme_name   VARCHAR(50) NOT NULL
     
  ); 
"""
cursor.execute(sql)

cursor.execute("""
CREATE TABLE Sous_Theme
  ( 
    id_sous_theme    SERIAL PRIMARY KEY NOT NULL,
    id_theme      INT NOT NULL, --fk--
    sous_theme_name    TEXT NOT NULL,
    FOREIGN KEY(id_theme) REFERENCES Theme(id_theme)
  );
""")

connection.commit()
connection.close()

# Chemin du répertoire
#chemin = "D:/archive/Kaggle/target_tables"
# ou chemin = "D:\\archive\\Kaggle\\target_tables"
chemin = "/users/2023/ds1/share/CORD-19/Kaggle/target_tables"

# Utilisation de la fonction listdir() pour obtenir tous les éléments du répertoire
elements = os.listdir(chemin)

# Filtrer les éléments pour récupérer seulement les dossiers
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin, element))]

try:
	# Connect to an existing database
	connection = psycopg2.connect("host=data dbname=zbalikci user=zbalikci password=zbalikci")
	cursor = connection.cursor()

	for dossier in dossiers[1:-1]:
		theme=(dossier[2:].replace("_"," ")).upper()
		cursor.execute("""
		INSERT INTO Theme(theme_name)
		VALUES(%s)
		RETURNING id;
		""",
		(theme,)) # IMPORTANT LORSQU'IL Y A UN SEUL VALEUR !!! RAJOUTER VIRGULE , !!!!
		id_theme=cursor.fetchone()[0]
		
		# Définir le chemin du dossier dont vous voulez récupérer les noms de fichiers
		#chemin = f'D:/archive/Kaggle/target_tables/{dossier}'
		chemin = f'/users/2023/ds1/share/CORD-19/Kaggle/target_tables/{dossier}'
		# Utiliser la fonction listdir() pour récupérer une liste des fichiers dans le dossier
		elements = os.listdir(chemin)
		for element in elements :
			cursor.execute("""
			INSERT INTO  Sous_Theme(sous_theme_name,id_theme)
			VALUES(%s,%s);
			""",
			(f'{element[:-4]}',id_theme))
			
	connection.commit()
	connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)


"""
#df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

#for i in range(100):
#	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')

# Ouvrir le fichier JSON
with open('/users/2023/ds1/share/CORD-19/document_parses/pdf_json/0000b6da665726420ab8ac9246d526f2f44d5943.json', 'r') as f:
    data = json.load(f)

# Accéder aux données dans le fichier JSON
valeur = data['metadata']['authors'][0]['affiliation']['institution']
# Afficher les données extraites
print(valeur)
print(type(valeur))

"""

