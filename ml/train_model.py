import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the dataset
dataset_folder = 'ml/datasets'
train = pd.read_csv(dataset_folder + '/train.csv')
test = pd.read_csv(dataset_folder + '/test.csv')

# get x and y (also don't need title here)
x_train = train.drop(['Quality', 'Title'], axis=1)
y_train = train['Quality']

x_test = test.drop(['Quality', 'Title'], axis=1)
y_test = test['Quality']

# Train and test models
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier

models = {
    'linreg':  LinearRegression(),
    'svr': SVR(kernel='rbf', C=1e3, gamma=0.1),
    'tree': DecisionTreeClassifier(criterion='entropy', random_state=0)
}

used_model = 'tree'
model = models[used_model]
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

# Print report
import sklearn.metrics as metrics

def print_regression_report(y, y_pred):
    print('Mean squared error: %.2f' % metrics.mean_squared_error(y, y_pred))
    print('Explained variance score: %.2f' % metrics.explained_variance_score(y, y_pred))
    print('R2 score: %.2f' % metrics.r2_score(y, y_pred))


def print_classification_report(y, y_pred):
    print(metrics.classification_report(y, y_pred))

print_classification_report(y_test, y_pred)

# Save model 
import pickle
with open('ml/models/' + used_model + '.pkl', 'wb') as f:
    pickle.dump(model, f)




