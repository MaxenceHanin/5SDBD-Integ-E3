"""
Here we use sklearn clustering to identify groups of users with similar habits,
or trips with similar characteristics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import sklearn.metrics as metrics

# https://stats.stackexchange.com/questions/52625/visually-plotting-multi-dimensional-cluster-data

df = pd.read_csv("../datasets/JC-201908-citibike-tripdata.csv")

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

classifier = KMeans(n_clusters=n_clusters, init="k-means++").fit(dataset)

labels = classifier.labels_

print(labels)

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

# print(get_cluster_stats(dataset, labels, True))

#### Visualization

print(list(zip(*np.unique(labels, return_counts=True))))

lbl_dataset = dataset.copy()
lbl_dataset["labels"] = labels
groups = lbl_dataset.groupby("labels")

# Plot
fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    group["weekday"].value_counts().plot(marker='+', linestyle='-', ms=6, label=name)
    # ax.plot(group["start station latitude"], group["start station longitude"], marker='o', linestyle='', ms=3, label=name)
    # ax.plot(group["end station latitude"], group["end station longitude"], marker='+', linestyle='', ms=3, label=name)
ax.legend()

plt.show()
