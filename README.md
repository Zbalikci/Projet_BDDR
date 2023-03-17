# M1 Data Science - Projet BDDR (2022 - 2023)

### Binôme Zeynep BALIKCI et Mariama MBAYE


Le sujet se trouve dans 1_Sujet.pdf

Lien utile : 

https://www.sqlalchemy.org/

Le schéma (schema.pdf) a été crée sur le site : https://dbdiagram.io/d   grâce au script dans le fichier : diagram_script.txt

#### Etape pour commencer le projet:

##### Etape 1 : commande shell 

django-admin startproject projet_bddr

##### Etape 2 : modifier le ./projet_bddr/projet_bddr/settings.py 

DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.postgresql',
        
        'NAME': 'covid19',
        
        'USER': 'postgres',
        
        'PASSWORD': 'Zor.bulursun1',
        
        'HOST': 'localhost',
        
        'PORT': '5432',
        
        }
}

##### Etape 3 : commande shell 

cd projet_bddr

python manage.py migrate

python manage.py startapp appli_covid19

##### Etape 4 : modifier le ./projet_bddr/projet_bddr/settings.py 

Il faut ensuite référencer cette application dans le projet.

Pour cela, on ajoute le nom de la classe 'appli_covid19.apps.AppliCovid19Config' dans la liste INSTALLED_APPS définie dans le fichier ./projet_bddr/projet_bddr/settings.py

##### Etape 5 : changer le ./projet_bddr/appli_covid19/models.py

Copier coller le fichier models.py disponible dans le git

##### Etape 6 : commande shell 

python manage.py makemigrations appli_covid19

python manage.py migrate



