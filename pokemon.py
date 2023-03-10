#!/bin/env python3

import pandas as pd
import logging
import psycopg2

df=pd.read_csv("/users/2023/ds1/122003362/Téléchargements/pokedex_05.20.csv")
L=df["type_1"].unique()


try:
    # Connect to an existing database
    connection = psycopg2.connect("host=data dbname=zbalikci user=zbalikci password=zbalikci")
    cursor = connection.cursor()
    
    type_id_liste={}

    for i in L:
        t:str = str(i)
        cursor.execute("""
        INSERT INTO public.type(name)
        VALUES(%s)
        RETURNING type_id;
        """,
        (t,)) # IMPORTANT LORSQU'IL Y A UN SEUL VALEUR !!! RAJOUTER VIRGULE , !!!!
        type_id=cursor.fetchone()[0]
        type_id_liste[t]=type_id

    for i in range(len(df)):

        cursor.execute("""
            INSERT INTO public.pokemon(name, name_de, generation, height, weight)
            VALUES(%s,%s,%s,%s,%s)
            RETURNING pokemon_id;
            """,
            (f'{df["name"][i]}', f'{df["german_name"][i]}', 
            f'{df["generation"][i]}',f'{df["height_m"][i]}',f'{df["weight_kg"][i]}'))
        pokemon_id=cursor.fetchone()[0]

        for l in L:
            if df["type_1"][i]==l:
                type_id=type_id_liste[l]
        cursor.execute("""
        INSERT INTO public.pokemon_type(pokemon_id,type_id)
        VALUES(%s,%s);
        """,
        (f'{pokemon_id}',f'{type_id}'))

    connection.commit()
    connection.close()

except Exception as e:
    logging.error("database connection failed")
    logging.error(e)


"""
ALTER TABLE public.pokemon ALTER COLUMN name type varchar(100); 
"""