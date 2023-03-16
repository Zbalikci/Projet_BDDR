#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 21:43:28 2023

@author: mariamadiabymbaye
"""
# J ai réussi à conecter la base psql avec django sur mon ordi. Il ya un truc à régler dans les settings pour qu'il crée la base.
# Ça c'est le peuplement pour theme et sous thème. je vais faire le reste demain.


from monappli.models import Theme, Sous_theme
import os

f = "/Users/mariamadiabymbaye/Downloads/kaggle/target_tables"
elements = os.listdir(f)
dossiers = [element for element in elements if os.path.isdir(os.path.join(f, element))]
for i in dossiers :
    themei= Theme()
    themei.theme_name = (i[2:].replace("_"," ")).upper()
    themei.save()
    chemin = f'{f}/{i}'
    elements = os.listdir(chemin)
    for j in elements:
        sousthemei = Sous_theme()
        sousthemei.soustheme_name = j[:-4]
        sousthemei.theme = themei
        sousthemei.save()
        
			
