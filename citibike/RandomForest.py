#!/usr/bin/env python
# coding: utf-8

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from time import time
from pymongo import MongoClient

import pickle
import csv
import os
import numpy as np
import pandas as pd


# In[25]:
file1 = pd.read_csv('clustered_stations.csv', sep=",")
file1.drop(labels="t", axis=1, inplace=True)
file1.drop(labels="name", axis=1, inplace=True)
file1.drop(labels="docks", axis=1, inplace=True)
file1.drop(labels="latitude", axis=1, inplace=True)
file1.drop(labels="longitude", axis=1, inplace=True)
file1.drop(labels="address", axis=1, inplace=True)
file1.drop(labels="color", axis=1, inplace=True)

#lecture csv data
file2 = pd.read_csv('res_201801.csv', sep=",")
file2.drop(labels="duration", axis=1, inplace=True)
file2.drop(labels="distance", axis=1, inplace=True)
file2.drop(labels="lat_o", axis=1, inplace=True)
file2.drop(labels="long_o", axis=1, inplace=True)
file2.drop(labels="lat_d", axis=1, inplace=True)
file2.drop(labels="long_d\t", axis=1, inplace=True)

result = pd.merge(file2, file1, how='outer', left_on='id_d', right_on='id').dropna()
taille_ech = 20000
y = result["cluster"][0:taille_ech]
result.drop(labels="id_d", axis=1, inplace=(True))
result.drop(labels="id", axis=1, inplace=(True))
result.drop(labels="cluster", axis=1, inplace=(True))

x = result[0:taille_ech]

test_size=0.3
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=test_size)

#Algo Random forest

model = RandomForestClassifier(min_samples_leaf=1, random_state=0, n_estimators = 10)
model.fit(X_train, Y_train)


def save_model_to_db(model, client, db, dbconnection, model_name, id_model):
    pickled_model = pickle.dumps(model)
    
    myclient = MongoClient(client)
    
    mydb = myclient[db]
    
    mycon = mydb[dbconnection]
    info = mycon.insert_one({'idS': id_model, 'model': pickled_model, 'name': model_name})
    print(info.inserted_id, ' saved with this id successfully!')

client = "mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority"
db = "CitiBike"
dbconnection = 'Models'
save_model_to_db(model, client, db, dbconnection, model_name="Random_Forest_Model", id_model=70)
