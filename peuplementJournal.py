#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:53:15 2023

@author: mmbay
"""

import json
import os
#from monappli.models import Affiliation
#from django.db import IntegrityError
import pandas as pd


df = pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")
df
m = df["journal"].unique()
for i in range(len(df["journal"])):
    print(f'journal = {df["journal"][i]}')
#	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} 
