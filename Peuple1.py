#!/bin/env python3
import pandas as pd
import logging
import psycopg2
import os
import json
import unidecode  
from django.db import models
"""
Pour peupler les tables theme, sous_theme, studytype, affiliation et journal:
"""
print("Où se trouve vos fichiers/dossiers Kaggle, documents_parses et metadata.csv ?")
chemin_archive = input("Veuillez donner le chemin : chemin_archive (/users/2023/ds1/share/CORD-19)=") or "/users/2023/ds1/share/CORD-19"
host=input("HOST (data)=") or "data"
dbname=input("DB_NAME (zbalikci)=") or "zbalikci"
user=input("USER_NAME (zbalikci)=") or "zbalikci"
password=input("PASSWORD (zbalikci)=") or "zbalikci"
############################################    Chargement des données nécessaires    ############################################
chemin_tables=f'{chemin_archive}/Kaggle/target_tables'
elements = os.listdir(chemin_tables)
dossiers = [element for element in elements if os.path.isdir(os.path.join(chemin_tables, element))]
chemin1 = f'{chemin_archive}/document_parses/pdf_json'
elements1 = os.listdir(chemin1)
print("En train de charger le fichier metadata.csv")
df=pd.read_csv(f'{chemin_archive}/metadata.csv')
print("En train de récupérer la liste des journaux dans metadata.csv")
### Liste des journaux
journaux=df[df['journal'].notnull()]['journal'].unique()
print("En train de crée la liste pour peupler la table studytype")
### Liste des types de publications
liste=pd.Series([])
for dossier in dossiers[1:-1]:
	chemin = f'{chemin_tables}/{dossier}'
	elements = os.listdir(chemin)
	for element in elements :
		df=pd.read_csv(f'{chemin}/{element}')
		if 'Study Type' in df:
			types=df[df['Study Type'].notnull()]['Study Type']
			liste=pd.concat([liste , types])
liste=liste.unique()
#####################################################################################################################################
print("\n ------ PEUPLEMENT DEBUT ------ \n")
try:
    connection = psycopg2.connect(f'host={host} dbname={dbname} user={user} password={password}')
    cursor = connection.cursor()
    #######################################################    LES "NULL"    ########################################################
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
    ##################################################    SOUS_THEMES et THEMES    ####################################################
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
    #########################################################    STUDYTYPE    ##########################################################
    print('peuplement de la table studytype : début')
    for study in liste:
        cursor.execute("""SELECT * FROM appli_covid19_studytype WHERE name LIKE %s""", (str(study),))
        records = cursor.fetchall()
        if records==[]:
            cursor.execute("""INSERT INTO appli_covid19_studytype(name) VALUES(%s);""",(str(study),))
    print('peuplement de la table studytype : fin')
    ##########################################################    JOURNAL    ###########################################################
    print('peuplement de la table journal : début')
    I=0
    for journal in journaux:
        s=journal
        if ("\\" in r"%r" % f"{s}" ):
            jo=unidecode.unidecode("".join(list(filter(str.isalpha,f"{s}"))))
        elif type(s)==float:
            jo='NULL'
        else:
            jo=s
        cursor.execute("""SELECT * FROM appli_covid19_journal WHERE name LIKE %s""", (jo,))
        records = cursor.fetchall()
        if records==[]:
            I+=1
            cursor.execute("""INSERT INTO appli_covid19_journal(id_journal ,name) VALUES(%s,%s);""",(I,jo))
    print('peuplement de la table journal : fin')
    ########################################################    AFFILIATION    #########################################################
    print('peuplement de la table affiliation : début')
    fichier=0
    for element in elements1:
        with open(f'{chemin1}/{element}', 'r') as f:
            data = json.load(f)
            fichier+=1
            print("AFFILIATION : nombre de pdf_json_files traités=",fichier)
            L=data['metadata']['authors']
            if len(L)!=0:
                for i in range(len(L)):
                    l= L[i]['affiliation']
                    if l!={}:
                        if l['institution'] == '':
                            name = unidecode.unidecode(l['laboratory'])
                            typ='laboratory'
                        elif l['laboratory']== '':
                            name = unidecode.unidecode(l['institution'])
                            typ='institution'
                        else:
                            name=[]
                            name.append(unidecode.unidecode(l['laboratory']))
                            name.append(unidecode.unidecode(l['institution']))
                        if l['location']!={} and ('country' in l['location']) :
                            country = ', '.join(list(set(l['location']['country'].split(', '))))
                        else:
                            country='NULL'
                        if type(name) == list:
                            if 'Complete List of Authors' not in name[0]:
                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name[0]),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name[0]),'laboratory'.upper(),country.upper()))
                            if 'Complete List of Authors' not in name[1]:
                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name[1]),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name[1]),'institution'.upper(),country.upper()))
                        else:
                            if 'Complete List of Authors' not in name:
                                cursor.execute("""SELECT * FROM appli_covid19_affiliation WHERE name LIKE %s""", (str(name),))
                                records = cursor.fetchall()
                                if records==[]:
                                    cursor.execute("""INSERT INTO appli_covid19_affiliation(name,type,country) VALUES(%s,%s,%s);""",(str(name),typ.upper(),country.upper()))
    print('peuplement de la table affiliation : fin')
    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)
print("\n ------ PEUPLEMENT FIN ------ \n")
