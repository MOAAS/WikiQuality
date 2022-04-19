import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset_folder = 'ml/datasets'
models_folder = 'ml/models'
dataset_name = '6000x6-csrh'

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
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


# Model names ending with c are classification models, and ending with r are regression models
models = {
    # models with very poor performance. will need to investigate
    'logreg_r': LogisticRegression(max_iter=10000),
    'svr_r': SVR(kernel='rbf', C=0.5, gamma='auto'),
    'svc_c': SVC(kernel='rbf', C=0.5, gamma='auto'),

    'linreg_r':  LinearRegression(),
    'tree_c': DecisionTreeClassifier(criterion='entropy', random_state=0, max_depth=15),
    'forest_c': RandomForestClassifier(n_estimators=150, criterion='entropy', random_state=0, max_depth=15),
    'tree_r': DecisionTreeRegressor(criterion='squared_error', random_state=0, max_depth=15),
    'forest_r': RandomForestRegressor(n_estimators=150, criterion='squared_error', random_state=0, max_depth=15),
}

used_model = 'tree_r'
model = models[used_model]
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

# Print report
import sklearn.metrics as metrics

def print_regression_report(y, y_pred):
    print("---------- REGRESSION REPORT ----------")
    print('Root mean squared error (RMSE):', np.sqrt(metrics.mean_squared_error(y, y_pred)))
    print('Mean squared error (MSE): %.2f' % metrics.mean_squared_error(y, y_pred))
    print('Mean absolute error (MAE): %.2f' % metrics.mean_absolute_error(y, y_pred))
    print('R2 score: %.2f' % metrics.r2_score(y, y_pred))

    # MSE per class?

    print("---------------------------------------")


def print_classification_report(y, y_pred):
    print(metrics.classification_report(y, y_pred))

if used_model.endswith('_c'):
    print_classification_report(y_test, y_pred)
else:
    print_regression_report(y_test, y_pred)

# Save model 
import pickle
with open(f'{models_folder}/{used_model}.pkl', 'wb') as f:
    pickle.dump(model, f)




