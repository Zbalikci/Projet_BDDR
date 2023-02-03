# M1 Data Science - Projet BDDR

#### Binôme Zeynep BALIKCI et Mariama MBAYE


Modélisation : Conceptuel ----> Logique
UML :

         ARTICLE:     
                      (psql)
article_id            serial                  pk
title                 varchar(50)  (ou text)
author                
publication_date      date
nb_pages              smallint
theme                 varchar(50)      


Nettoyage : Attention au doublon:
id     title
1      "abc"
2      "abc"
