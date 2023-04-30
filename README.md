# M1 Data Science - Projet BDDR (2022 - 2023)

## Binôme Zeynep BALIKCI et Mariama MBAYE


Le sujet se trouve dans 1_Sujet.pdf

Le schéma (3_Schema.pdf) a été crée sur le site : https://dbdiagram.io/d   grâce au script dans le fichier : 2_diagram_script.txt

### Etapes pour le projet:

- Etape 0 : créer une base de donnée sur pgAdmin ou utiliser une déjà existant et installer la librairie unidecode.

```bash
pip install unidecode
```

- Etape 1 : Télécharger tout le dossier disponible sur le git

- Etape 2 : Modifier DATABASES du fichier ./projet_bddr/projet_bddr/settings.py:
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
NAME, USER, HOST et PASSWORD sont à compléter par vos données.

- Etape 3 : Commandes shell 
```bash
cd projet_bddr
```
```bash
python manage.py makemigrations appli_covid19
```
```bash
python manage.py migrate
```

- Etape 4 : Commencer le peulement de la base de donnée 
- Etape 4.1 : Pour peupler les tables theme, sous_theme, studytype, affiliation et journal

Exécuter le fichier Peuple1.py sur le shell normal (pas besoin de changer quoi que soit dans le script du fichier).

Entrer les informations nécessaires demandé après l'exécution : chemin_archive, host, etc...

Exemples : chemin_archive = /users/2023/ds1/share/CORD-19

HOST = data

DB_NAME = zbalikci

USER_NAME = zbalikci 

PASSWORD = zbalikci

Le peuplement de ces tables est terminé au bout d'1 heure et 10 min environ.

- Etape 4.2 : Pour peupler les tables les tables articles, article_theme et studytype_articles.

Exécuter le fichier Peuple2.py du dossier projet_bddr, pour cela vous devez utilisez le shell de DJANGO avec : 

```bash
python manage.py shell
```
Linux :
```bash
run Peuple2.py
```
Windows Powershell:
```bash
exec(open('Peuple2.py').read())
```
Le peuplement de ces tables est terminé au bout d'1 heure et 30 min environ.

- Etape 4.3 : Pour peupler les tables les tables authors, author_affiliation et author_article.

Exécuter le fichier Peuple3.py du dossier projet_bddr, pour cela vous devez utilisez le shell de DJANGO avec :  
```bash
python manage.py shell
```
Linux :
```bash
run Peuple3.py
```
Windows Powershell:
```bash
exec(open('Peuple3.py').read())
```
Le peuplement de ces tables est terminée au bout 5h environ. (Début 18h)
