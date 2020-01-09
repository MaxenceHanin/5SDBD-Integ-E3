#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from time import time

import pickle
import pandas as pd
import csv
import os
import numpy as np


# In[25]:


#lecture csv 
file = pd.read_csv('res_201801.csv', sep=",", names=["id_o", "id_d", "dur", "dis", "h", "w", "m", "typ", "gen", "age", "lat_o", "long_o", "lat_d", "long_d"])

file.drop(labels="dur", axis=1, inplace=True)
file.drop(labels="dis", axis=1, inplace=True)
file.drop(labels="lat_o", axis=1, inplace=True)
file.drop(labels="long_o", axis=1, inplace=True)
file.drop(labels="lat_d", axis=1, inplace=True)
file.drop(labels="long_d", axis=1, inplace=True)
y = file["id_d"]
file.drop(labels="id_d", axis=1, inplace=(True))
x = file

test_size=0.3
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=test_size)
#Algo Random forest

begin = time()
model = RandomForestClassifier(max_depth=15, random_state=0, n_estimators=200)
model.fit(X_train, Y_train)
end = time()

print("Score : ", model.score(X_test, Y_test))
print("Temps d'execution : ", end-begin)

#Sauvegarde modele 
filename = 'model_random_forest.sav'
pickle.dump(model, open(filename, 'wb'))

#load model
#loaded_model = pickle.load(open(filename, 'rb'))
