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

data =pd.read_csv("/Users/mariamadiabymbaye/Downloads/metadata2.csv",
                  usecols=['title','publish_time','abstract','url','journal'])

# Remplissage table Arcticles
for i in range(len(data['title'])):
    ##### Journal#####
    un_journal = Journal()
    try:
       un_journal.name = data['journal'][i]
       un_journal.save()
    except IntegrityError:
        un_journal = Journal.objects.get(name = data['journal'][i])
        
    ###### Articles #####
    un_article = Articles()
    un_article.title = data['title'][i]
    #formats = ['%Y-%m-%d', '%Y']
    #for forma in formats:
    try :
       un_article.publication_date = datetime.strptime(data['publish_time'][i], '%Y-%m-%d')
    except:
        pass
   # la il met rien quand c'est le format '%Y'
    un_article.abstract = data['abstract'][i]
    un_article.stulink = data['url'][i]
    un_article.journal = un_journal
    un_article.save()

    
    
