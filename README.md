# M1 Data Science - Projet BDDR (2022 - 2023)

## Binôme Zeynep BALIKCI et Mariama MBAYE


Le sujet se trouve dans 1_Sujet.pdf

Le schéma (3_schema.pdf) a été crée sur le site : https://dbdiagram.io/d   grâce au script dans le fichier : 2_diagram_script.txt

### Etapes pour le projet:

- Etape 0 : créer une base de donnée sur pgAdmin ou utiliser une déjà existant. 

- Etape 1 : commande shell 
```bash
django-admin startproject projet_bddr
```
- Etape 2 : modifier DATABASES du fichier ./projet_bddr/projet_bddr/settings.py  par :
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'A_COMPLETER!',
        'USER': 'A_COMPLETER!',
        'PASSWORD': 'A_COMPLETER!',
        'HOST': 'A_COMPLETER!',
        'PORT': '5432',
        }
}
```
- Etape 3 : commandes shell 
```bash
cd projet_bddr
```
```bash
python manage.py migrate
```
```bash
python manage.py startapp appli_covid19
```
- Etape 4 : modifier le ./projet_bddr/projet_bddr/settings.py 

Il faut ensuite référencer cette application dans le projet.

Pour cela, on ajoute le nom de la classe 'appli_covid19.apps.AppliCovid19Config' dans la liste INSTALLED_APPS définie dans le fichier ./projet_bddr/projet_bddr/settings.py

- Etape 5 : changer le fichier ./projet_bddr/appli_covid19/models.py

Copier coller le fichier models.py disponible dans le git

- Etape 6 : commande shell 
```bash
python manage.py makemigrations appli_covid19
```
```bash
python manage.py migrate
```

- Etape 7 : Commencer le peulement de la base de donnée 
- Etape 7.1 : Pour peupler les tables theme, sous_theme, studytype, affiliation et journal

Premièrement télécharger et lancer le fichier Peuple1.py sur le shell (pas besoin de changer quoi que soit dans le script du fichier).

Entrer les informations nécessaires demandé au lancement : chemin_archive, host, etc...

Exemples : chemin_archive = /users/2023/ds1/share/CORD-19

HOST = data

DB_NAME = zbalikci

USER_NAME = zbalikci 

PASSWORD = zbalikci

Le peuplement est terminée au bout d'1 heure et 20 min environ.

- Etape 7.2 (en cours) : Pour peupler les tables les tables articles, article_theme, studytype_articles, authors, author_affiliation et author_article.

```bash
pip install unidecode
```
Télécharger le fichier Peuple2.py dans le dossier projet_bddr

Lancer le fichier Peuple2.py sur le shell de DJANGO avec : 
```bash
python manage.py shell
```
```bash
run Peuple2.py
```
