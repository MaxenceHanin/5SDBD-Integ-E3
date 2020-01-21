import pandas as pd
import numpy as np
import operator
import collections
import logging

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics


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
            
            if len(props) != 0:
                val = max(props.items(), key=operator.itemgetter(1))[0]
            else:
                val = -1
            
            predictions.append(val)
            
        return np.array(predictions)
        

# This class is totally unfinished and unusable
class CitibikeEstimator:
    def __init__(self):
        self.precise_estimator = StatisticEstimator()
        self.general_estimator = StatisticEstimator()
        
    def fit(self, data, targets):
        self.precise_estimator.fit(data, targets)
        self.general_estimator.fit(data[["start station id"]], targets)
    
    def predict(self, data):
        precise_preds = self.precise_estimator.predict(data)
        general_preds = self.general_estimator.predict(data[["start station id"]])
        # TODO
        return general_preds


### Preprocessing

def add_time(df):
    # Create hour and weekday from starttime
    df["date"] = pd.to_datetime(df["starttime"])
    df["hour"] = df["date"].dt.hour
    df["weekday"] = df["date"].dt.weekday


def with_clusters(data):
    clusters = pd.read_csv("../datasets/clustered_stations.csv")
    data = pd.merge(data, clusters[["id", "cluster"]], left_on="start station id", right_on="id")
    data = pd.merge(data, clusters[["id", "cluster"]], left_on="end station id", right_on="id", suffixes=("", " end"))
    return data


### GENERAL TEST METHODS

def test_estimator(df, featuresCols, labelsCols):
    train_df, test_df = train_test_split(df, test_size=0.2)

    train_features = train_df[featuresCols]
    train_labels = train_df[labelsCols]
    test_features = test_df[featuresCols]
    test_labels = test_df[labelsCols]

    logging.info("Dataset preprocessed!")

    # Test estimator
    estimator = StatisticEstimator()
    estimator.fit(train_features, train_labels)

    logging.info("Training done!")

    test_predictions = estimator.predict(test_features)
    accuracy = metrics.accuracy_score(test_labels.values.reshape(-1), test_predictions)

    print("Precision score = %f" % (accuracy,))


### TESTS

def test_next_station(df):
    # Create hour and weekday from starttime
    df["date"] = pd.to_datetime(df["starttime"])
    df["hour"] = df["date"].dt.hour
    df["weekday"] = df["date"].dt.weekday
    
    featuresCols = ["hour", "weekday", "start station id"]
    labelsCols = ["end station id"]
    
    test_estimator(df, featuresCols, labelCols)


def test_clusters(data):
    data = with_clusters(data)
    
    labels = data["cluster"]
    predictions = data["cluster end"]
    
    accuracy = metrics.accuracy_score(labels.values.reshape(-1), predictions.values.reshape(-1))
    
    print("Precision score = %f" % (accuracy,))

def test_id_to_clusters(data):
    add_time(data)
    data = with_clusters(data)
    
    featuresCols = ["start station id"]
    labelsCols = ["cluster end"]
    
    test_estimator(data, featuresCols, labelsCols)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    df = pd.read_csv("../datasets/201801.csv")
    logging.info("Dataset loaded!")

    test_id_to_clusters(df)
    