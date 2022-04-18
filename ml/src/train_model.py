import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset_folder = 'ml/datasets'
models_folder = 'ml/models'
dataset_name = '4000x6-csrhn'

# load the dataset
train = pd.read_csv(f'{dataset_folder}/{dataset_name}_train.csv')
test = pd.read_csv(f'{dataset_folder}/{dataset_name}_test.csv')

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

used_model = 'linreg'
model = models[used_model]
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

# Print report
import sklearn.metrics as metrics

def print_regression_report(y, y_pred):
    print('Mean squared error: %.2f' % metrics.mean_squared_error(y, y_pred))
    print('Mean absolute error: %.2f' % metrics.mean_absolute_error(y, y_pred))

    print('Explained variance score: %.2f' % metrics.explained_variance_score(y, y_pred))
    print('R2 score: %.2f' % metrics.r2_score(y, y_pred))


def print_classification_report(y, y_pred):
    print(metrics.classification_report(y, y_pred))

print_regression_report(y_test, y_pred)

# Save model 
import pickle
with open(f'{models_folder}/{used_model}.pkl', 'wb') as f:
    pickle.dump(model, f)




