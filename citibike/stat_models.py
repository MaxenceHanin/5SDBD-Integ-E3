import pandas as pd
import numpy as np
import operator
import collections

from sklearn.cluster import KMeans
import sklearn.metrics as metrics

# https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary

df = pd.read_csv("../datasets/JC-201909-citibike-tripdata.csv")

# Create hour and weekday from starttime
df["date"] = pd.to_datetime(df["starttime"])
df["hour"] = df["date"].dt.hour
df["weekday"] = df["date"].dt.weekday

features = df[["hour", "weekday", "start station id"]]
labels = df[["end station id"]]

print(df.iloc[0])

class StatisticEstimator:
    def __init__(self):
        self.counts = collections.defaultdict(lambda: collections.defaultdict(int))
        self.total = 0
        
    def fit(self, data, targets):
        n = data.shape[0]
        
        for i in range(n):
            key = tuple(data.iloc[i])
            target = targets.iloc[i,0]
            self.counts[key][target] += 1
        
        self.total += n
        
    def predict(self, data):
        predictions = []
        n = data.shape[0]
        
        for i in range(n):
            key = tuple(data.iloc[i])
            props = self.counts[key]
            val = max(props.iteritems(), key=operator.itemgetter(1))[0]
            predictions.append(val)
            
        return np.array(predictions)
        
if __name__ == "__main__":
    estimator = StatisticEstimator()
    estimator.fit(features, labels)

    print(len(estimator.counts), estimator.total)