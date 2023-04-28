# M1 Data Science - Projet BDDR (2022 - 2023)

## Binôme Zeynep BALIKCI et Mariama MBAYE


Le sujet se trouve dans 1_Sujet.pdf

Le schéma (3_schema.pdf) a été crée sur le site : https://dbdiagram.io/d   grâce au script dans le fichier : 2_diagram_script.txt

### Etapes pour le projet:

- Etape 0 : créer une base de donnée sur pgAdmin ou utiliser une déjà existant et installer la librairie unidecode.

```bash
pip install unidecode
```

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

Le peuplement de ces tables est terminé au bout d'1 heure et 20 min environ.

- Etape 7.2 : Pour peupler les tables les tables articles, article_theme et studytype_articles.

Télécharger le fichier Peuple2.py dans le dossier projet_bddr

Lancer le fichier Peuple2.py sur le shell de DJANGO avec : 
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
Le peuplement de ces tables est terminé au bout d'1 heure et 20 min environ.

- Etape 7.3 (en cours) : Pour peupler les tables les tables authors, author_affiliation et author_article.

Télécharger le fichier Peuple3.py dans le dossier projet_bddr

Lancer le fichier Peuple3.py sur le shell de DJANGO avec : 
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
Le peuplement de ces tables est terminée au bout ..... environ.

début 14h22

DROP TABLE appli_covid19_affiliation, appli_covid19_article_theme, appli_covid19_articles, appli_covid19_author_affiliation, appli_covid19_author_article, appli_covid19_authors, appli_covid19_journal, appli_covid19_sous_theme;
DROP TABLE appli_covid19_studytype, appli_covid19_theme, auth_group, auth_group_permissions, auth_permission, auth_user, auth_user_groups,auth_user_user_permissions, django_admin_log, django_content_type, django_migrations, django_session;

