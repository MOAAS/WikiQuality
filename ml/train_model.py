import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

# load the dataset
dataset_folder = 'ml/datasets'
train = pd.read_csv(dataset_folder + '/train.csv')
test = pd.read_csv(dataset_folder + '/test.csv')

# get x and y (also don't need title here)
x_train = train.drop(['Quality', 'Title'], axis=1)
y_train = train['Quality']

x_test = test.drop(['Quality', 'Title'], axis=1)
y_test = test['Quality']

# train with decision tree
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x_train, y_train)

# test model
y_pred = clf.predict(x_test)
print(sklearn.metrics.classification_report(y_test, y_pred))

# save model with pickle
import pickle
with open('ml/models/decision_tree.pkl', 'wb') as f:
    pickle.dump(clf, f)




