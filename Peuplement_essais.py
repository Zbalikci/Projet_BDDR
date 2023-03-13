"""
Pour peupler les tables themes et sujets :

"""

import os

# Chemin du répertoire

chemin = "D:/archive/Kaggle/target_tables"
# ou chemin = "D:\\archive\\Kaggle\\target_tables"

# Utilisation de la fonction listdir() pour obtenir tous les éléments du répertoire
elements = os.listdir(chemin)

# Filtrer les éléments pour récupérer seulement les dossiers
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin, element))]
for dossier in dossiers[1:-1]:
    # Définir le chemin du dossier dont vous voulez récupérer les noms de fichiers
    chemin = f'D:/archive/Kaggle/target_tables/{dossier}'
    # Utiliser la fonction listdir() pour récupérer une liste des fichiers dans le dossier
    elements = os.listdir(chemin)
    for element in elements :
        print(element[:-4])
    
 
#!/bin/env python3
import pandas as pd
import logging
import psycopg2

df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

for i in range(100):
	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')

	
	

import json

# Ouvrir le fichier JSON
with open('/users/2023/ds1/share/CORD-19/document_parses/pdf_json/0000b6da665726420ab8ac9246d526f2f44d5943.json', 'r') as f:
    data = json.load(f)

# Accéder aux données dans le fichier JSON
valeur = data['metadata']['authors'][0]['affiliation']['institution']
# Afficher les données extraites
print(valeur)
print(type(valeur))

