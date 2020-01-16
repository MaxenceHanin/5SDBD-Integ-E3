#!/usr/bin/env python
# coding: utf-8

# In[22]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from time import time

import pickle
import pandas as pd
import csv
import os
import numpy as np



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

result = pd.merge(file2, file1, how='outer', left_on='id_o', right_on='id').dropna()

y = result["cluster"][0:100000]
result.drop(labels="id_d", axis=1, inplace=(True))
result.drop(labels="id", axis=1, inplace=(True))
result.drop(labels="cluster", axis=1, inplace=(True))

x = result[0:100000]


# In[23]:


test_size=0.3
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=test_size)


# In[24]:


#Algo Random forest
min_sample = [0.0001,0.001,0.01,0.1,1,10]
estimator = [10,50,100,200]
for i in min_sample:
    for j in estimator:
        print("i : ", i)
        begin = time()
        model = RandomForestClassifier(min_samples_leaf=i, random_state=0, n_estimators = j)
        model.fit(X_train, Y_train)
        end = time()
        print("Contexte : Min_Samples_leaf : " + str(i) + " Estimator : " +str(j))
        print("Score : ", model.score(X_test, Y_test))
        print("Temps d'execution : ", end-begin)


# In[25]:


model = RandomForestClassifier(min_samples_leaf=1, random_state=0, n_estimators = 10)
model.fit(X_train, Y_train)


# In[20]:


print("Score : ", model.score(X_test, Y_test))
print("Temps d'execution : ", end-begin)


# In[10]:


print(result)


# In[15]:


pd.merge(file2, file1, how='outer', left_on='id_o', right_on='id').dropna()[200000:200001]


# In[16]:


result[200000:200001]


# In[14]:


model.predict(result[200000:200001])


# In[26]:


#Sauvegarde modele 
filename = 'model_random_forest.sav'
pickle.dump(model, open(filename, 'wb'))

#chargement model
#loaded_model = pickle.load(open(filename, 'rb'))


# In[4]:


def save_model_to_db(model, client, db, dbconnection, model_name):
    pickled_model = pickle.dumps(model)
    
    myclient = MongoClient(client)
    
    mydb = myclient[db]
    
    mycon = mydb[dbconnection]
    info = mycon.insert_one({model_name: pickled_model, 'name': model_name, 'created_time':time()})
    print(info.inserted_id, ' saved with this id successfully!')
    
    details = {
        'idM': 14,
        'model':model_name,
        'name': model_name
    }
    
    return (details)


# In[5]:


import panda as pd

client = "mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority"
db = "CitiBike"
dbconnection = 'Models'
save_model_to_db(model, client, db, dbconnection, model_name="test_RandomForest")


# In[ ]:




