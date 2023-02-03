# M1 Data Science - Projet BDDR

#### Binôme Zeynep BALIKCI et Mariama MBAYE


Nettoyage : Attention au doublon:

id     title

1      "abc"

2      "abc"


Modélisation : Conceptuel ----> Logique


UML :

              ARTICLE:          
                           (psql)                 
     article_id            serial                  pk
     title                 varchar(50)  (ou text)  
     author                                       
     publication_date      date                    
     nb_pages              smallint                
     sujet_id              varchar(50)             


              SUJET:                          
     sujet_id           serial           pk
     nom                varchar(50) 
     description        varchar
  
Relation Sujet Article n:m

Donc on peut faire à la place :

Relations :

Sujet - Sujet_Article 1:n

Sujet_Article - Article n:1



              SUJET:                          
     sujet_id           serial           pk
     nom                varchar(50)   

              SUJET_ARTICLE:                          
     sujet_id           serial           pk
     article_id         serial           pk
     
Tableau croisé pour Sujet-arcticle : 1 artcile peut avoir plusieurs sujet, plusieurs article traite d'un sujet.

              ARTICLE:                          
                           (psql)                 
     article_id            serial                  pk
     title                 varchar(50)  (ou text) 
     etc...

Autre groupe redondant : les auteurs, donc il faut créer un autre entité : auteur qui est relié a des articles : 1:n


https://www.postgresql.org/download/windows/

https://dbdiagram.io/d
