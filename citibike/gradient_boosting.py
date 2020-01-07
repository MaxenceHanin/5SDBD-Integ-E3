import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

#import data
full_data = pd.read_csv("res_201801",sep=",", names=["id_o", "id_d", "dur", "dis", "h", "w", "m", "typ", "gen", "age", "lat_o", "long_o", "lat_d", "long_d"])
full_data.drop(labels="dur", axis=1, inplace=True)
full_data.drop(labels="lat_d", axis=1, inplace=True)
full_data.drop(labels="long_d", axis=1, inplace=True)
full_data.drop(labels="dis", axis=1, inplace=True)



y_train = full_data["id_d"]

#split data
X_train = full_data #.values[0:1000]

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)

# seed used by the random number generator
state = 12  
test_size = 0.30  

#Split arrays or matrices into random train and test subsets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,  
    test_size=test_size, random_state=state)

#try setting different learning rates, compare the performance of the classifier's performance at different learning rates
 
lr_list = [0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]

for learning_rate in lr_list:
    gb_clf = GradientBoostingClassifier(n_estimators=20, learning_rate=learning_rate, max_features=2, max_depth=2, random_state=0)
    gb_clf.fit(X_train, y_train)

    print("Learning rate: ", learning_rate)
    print("Accuracy score (training): {0:.3f}".format(gb_clf.score(X_train, y_train)))
    print("Accuracy score (validation): {0:.3f}".format(gb_clf.score(X_val, y_val)))
	

	#from xgboost import XGBClassifier
	#xgb_clf = XGBClassifier()
	#xgb_clf.fit(X_train, y_train)
	#score = xgb_clf.score(X_val, y_val)
	#print(score)

