"""
Here we use sklearn clustering to identify groups of users with similar habits,
or trips with similar characteristics
"""

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
import sklearn.metrics as metrics

# https://stats.stackexchange.com/questions/52625/visually-plotting-multi-dimensional-cluster-data

df = pd.read_csv("../datasets/JC-201909-citibike-tripdata.csv")

# Create hour and weekday from starttime
df["date"] = pd.to_datetime(df["starttime"])
df["hour"] = df["date"].dt.hour
df["weekday"] = df["date"].dt.weekday

# select only some features
# add: "birth year", "gender" for suscribers
geographicalCols = ["start station latitude", "start station longitude", "end station latitude", "end station longitude"]
temporalCols = ["hour", "weekday"]
featuresCols = geographicalCols + temporalCols

dataset = df[featuresCols]


#### Clustering

n_clusters = 5

classifier = KMeans(n_clusters=n_clusters, init="k-means++")

labels = classifier.fit_predict(dataset)


#### Data analysis

def get_cluster_stats(dataset, labels, as_tuple=False):
    """
    Compute cluster center, variance, bounds, count
    """
    lbl_dataset = dataset.copy()
    lbl_dataset["labels"] = labels
    
    cluster_count = lbl_dataset.groupby("labels").count()
    cluster_min = lbl_dataset.groupby("labels").min()
    cluster_mean = lbl_dataset.groupby("labels").mean()
    cluster_max = lbl_dataset.groupby("labels").max()
    cluster_var = lbl_dataset.groupby("labels").var()
    
    if as_tuple:
        return cluster_count, cluster_min, cluster_mean, cluster_max, cluster_var
    else:
        result = pd.merge(cluster_count, cluster_min, on="labels", suffixes=(".count", ".min"))
        result = pd.merge(result, cluster_mean, on="labels", suffixes=("", ".mean"))
        result = pd.merge(result, cluster_max, on="labels", suffixes=("", ".max"))
        result = pd.merge(result, cluster_var, on="labels", suffixes=("", ".var"))
        return result

print(get_cluster_stats(dataset, labels, True))

#### Visualization