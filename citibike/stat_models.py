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
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    df = pd.read_csv("../datasets/JC-201909-citibike-tripdata.csv")
    logging.info("Dataset loaded!")

    # Create hour and weekday from starttime
    df["date"] = pd.to_datetime(df["starttime"])
    df["hour"] = df["date"].dt.hour
    df["weekday"] = df["date"].dt.weekday
    
    featuresCols = ["hour", "weekday", "start station id"]
    labelsCols = ["end station id"]
    
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
    