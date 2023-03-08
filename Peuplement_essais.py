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
    

