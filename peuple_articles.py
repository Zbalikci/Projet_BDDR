#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 15:05:30 2023

@author: mmbay
"""

from appli_covid19.models import Articles,Journal 
from django.db import IntegrityError
from datetime import datetime
import pandas as pd

data =pd.read_csv("/users/2023/ds1/121009626/Téléchargements/metadata2.csv",
                  usecols=['title','publish_time','abstract','url','journal'])

# Remplissage table Arcticles
for i in range(len(data)):
    ##### Journal#####
    un_journal = Journal()
    try:
       un_journal.name = data['journal']
       un_journal.save()
    except IntegrityError:
        un_journal = Journal.objects.get(name = data['journal'])
        
    ###### Articles #####
    un_article = Articles()
    un_article.title = data['title']
    formats = ['%Y-%m-%d', '%Y']
    for forma in formats:
        un_article.publication_date = data['publish_time'].apply(lambda x: datetime.strptime(x, forma))
    # fait un if si plusieurs format de date, mais si que 2 formats de dates fait un try/except
    #PROBLEME AU NIVEAU DE LA DATE : ValueError: time data '2008' does not match format '%Y-%m-%d'
    un_article.abstract = data['abstract']
    un_article.stulink = data['url']
    un_article.journal = un_journal
    un_article.save()
    

    
    
