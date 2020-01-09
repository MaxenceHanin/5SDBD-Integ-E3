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

df = pd.read_csv("../datasets/201801_clean.csv")

# print(df)

# select only some features
# add: "birth year", "gender" for suscribers
geographicalCols = ["lat_o","long_o","lat_d","long_d"]
temporalCols = ["hour", "weekday","duration"]
featuresCols = geographicalCols + temporalCols

dataset = df[featuresCols]


#### Clustering

n_clusters = 10

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

unique,counts=np.unique(labels,return_counts=True)
for i in range(len(unique)):
    print(unique[i],counts[i])

# print(list(zip(*np.unique(labels, return_counts=True))))

lbl_dataset = dataset.copy()
lbl_dataset["labels"] = labels
groups = lbl_dataset.groupby("labels")
# groups = lbl_dataset.groupby(["lat_o","long_o"])

# Plot
fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    # group["hour"].value_counts().plot(marker='+', linestyle='', ms=6, label=name)
    ax.plot(group["lat_o"], group["long_o"], marker='o', linestyle='', ms=3, label=name)
    ax.plot(group["lat_d"], group["long_d"], marker='+', linestyle='', ms=3, label=name)
    # plt.show()
ax.legend()

plt.show()
