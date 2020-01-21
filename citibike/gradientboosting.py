#!/usr/bin/env python
# coding: utf-8

# In[6]:


print("import lib")
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from pymongo import MongoClient

import xgboost
from time import time
import pickle
import csv
import os
import numpy as np
import pandas as pd


# In[24]:


print("Import data")
#import data
file = pd.read_csv('clustered_stations.csv', sep=",")
file.drop(labels="t", axis=1, inplace=True)
file.drop(labels="name", axis=1, inplace=True)
file.drop(labels="docks", axis=1, inplace=True)
file.drop(labels="latitude", axis=1, inplace=True)
file.drop(labels="longitude", axis=1, inplace=True)
file.drop(labels="address", axis=1, inplace=True)
file.drop(labels="color", axis=1, inplace=True)

file2 = pd.read_csv('res_201801.csv', sep=",")
file2.drop(labels="duration", axis=1, inplace=True)
file2.drop(labels="distance", axis=1, inplace=True)
file2.drop(labels="lat_o", axis=1, inplace=True)
file2.drop(labels="long_o", axis=1, inplace=True)
file2.drop(labels="lat_d", axis=1, inplace=True)
file2.drop(labels="long_d\t", axis=1, inplace=True)

result = pd.merge(file2, file, how='outer', left_on='id_d', right_on='id').dropna()

y = result["cluster"][1:500000]
result.drop(labels="id_d", axis=1, inplace=(True))
result.drop(labels="id", axis=1, inplace=(True))
result.drop(labels="cluster", axis=1, inplace=(True))

x = result[1:500000]

# seed used by the random number generator
state = 12  
test_size = 0.30  

#Split arrays or matrices into random train and test subsets
X_train, X_val, y_train, y_val = train_test_split(x, y,  
    test_size=test_size, random_state=state)

#try setting different learning rates, compare the performance of the classifier's performance at different learning rates
 
lr_list = [0.1] #[0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]
print("Start training")
'''
for learning_rate in lr_list:
    gb_clf = GradientBoostingClassifier()
    print("taille ", len(X_train), " : ", len(y_train))
    gb_clf.fit(X_train, y_train)

    print("Learning rate: ", learning_rate)
    print("Accuracy score (training): {0:.3f}".format(gb_clf.score(X_train, y_train)))
    print("Accuracy score (validation): {0:.3f}".format(gb_clf.score(X_val, y_val)))
'''
begin = time()
xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)
end = time()
score = xgb_clf.score(X_val, y_val)
print("time :", end-begin)
print(score)


def save_model_to_db(model, client, db, dbconnection, model_name, id_model):
    pickled_model = pickle.dumps(model)
    
    myclient = MongoClient(client)
    
    mydb = myclient[db]
    
    mycon = mydb[dbconnection]
    info = mycon.insert_one({'idS': id_model, 'model': pickled_model, 'name': model_name})
    print(info.inserted_id, ' saved with this id successfully!')
    


import pandas as pd

client = "mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority"
db = "CitiBike"
dbconnection = 'Models'
save_model_to_db(xgb_clf, client, db, dbconnection, model_name="Grad_Boost_Model", id_model=68)


