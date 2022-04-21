import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

dataset_folder = 'ml/datasets'
models_folder = 'ml/models'
dataset_name = '6000x6-csrhn'
#dataset_name = "small"

# load the dataset
train = pd.read_csv(f'{dataset_folder}/{dataset_name}_train.csv')
test = pd.read_csv(f'{dataset_folder}/{dataset_name}_test.csv')

quality_mapping_6class = { 5: 5,   4: 4,   3: 3,   2: 2,   1: 1,   0: 0 }
quality_mapping_3class = { 5: 2,   4: 2,   3: 1,   2: 1,   1: 0,   0: 0 }
quality_mapping_2class = { 5: 1,   4: 1,   3: 0,   2: 0,   1: 0,   0: 0 }
use_quality_mapping = quality_mapping_6class
use_categories = ["C", "S", "R", "H", "N"]

classes = list(set(use_quality_mapping.values()))

x_train = train.drop(['Quality', 'Title'], axis=1)
y_train = train['Quality'].replace(use_quality_mapping)

x_test = test.drop(['Quality', 'Title'], axis=1)
y_test = test['Quality'].replace(use_quality_mapping)

# Train and test models
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as metrics

from sklearn.preprocessing import StandardScaler  
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

# Model names ending with c are classification models, and ending with r are regression models
# Some models only have decent results with normalize data activated (e.g. logistic regression, svm, knn, neural network)
# Still, normalizing does not have a negative impact on the other algorithms, so keep it on
# Neural networks (MLP) should be experimented with different alphas [10^-7,10^-1] and other parameters too
models = {
    'tree_c': DecisionTreeClassifier(criterion='entropy', random_state=0, max_depth=15),
    'forest_c': RandomForestClassifier(n_estimators=150, criterion='entropy', random_state=0, max_depth=15),
    'ada_c': AdaBoostClassifier(n_estimators=150, random_state=0, learning_rate=0.1, base_estimator=DecisionTreeClassifier(max_depth=10)),
    'gboost_c': GradientBoostingClassifier(n_estimators=150, random_state=0, learning_rate=0.01),
    'knn_c': KNeighborsClassifier(n_neighbors=10),
    'svc_c': SVC(kernel='rbf', C=2, gamma='scale'),
    'mlp_c': MLPClassifier(hidden_layer_sizes=(100,), max_iter=10000, alpha=0.1, ),
    'gnb_c': GaussianNB(),

    'linreg_r': LinearRegression(),
    'tree_r': DecisionTreeRegressor(criterion='squared_error', random_state=0, max_depth=15),
    'forest_r': RandomForestRegressor(n_estimators=150, criterion='squared_error', random_state=0, max_depth=15),
    'ada_r': AdaBoostRegressor(n_estimators=150, random_state=0, learning_rate=0.1, base_estimator=DecisionTreeRegressor(max_depth=10)),
    'gboost_r': GradientBoostingRegressor(n_estimators=150, random_state=0, learning_rate=0.01),
    'logreg_r': LogisticRegression(max_iter=10000),
    'svr.1_r': SVR(kernel='rbf', C=0.1, gamma='scale'), # todo: experiment different C's again
    'svr1_r': SVR(kernel='rbf', C=1, gamma='scale'), # todo: experiment different C's again
    'svr2_r': SVR(kernel='rbf', C=2, gamma='scale'), # todo: experiment different C's again
    'svr10_r': SVR(kernel='rbf', C=10, gamma='scale'), # todo: experiment different C's again
    'svr100_r': SVR(kernel='rbf', C=100, gamma='scale'), # todo: experiment different C's again
    'mlp_r': MLPRegressor(hidden_layer_sizes=(100,), max_iter=10000, alpha=0.1,), 
}

def print_regression_report(y, y_pred):  
    print("------------------ OVERALL REPORT ------------------")
    print('Mean squared error (MSE): %.2f' % metrics.mean_squared_error(y, y_pred))
    print('Root mean squared error (RMSE):', np.sqrt(metrics.mean_squared_error(y, y_pred)))
    print('Mean absolute error (MAE): %.2f' % metrics.mean_absolute_error(y, y_pred))
    print('R2 score: %.2f' % metrics.r2_score(y, y_pred))

    print("----------------- PER-CLASS REPORT -----------------")
    print ("{:<10} {:<10} {:<10} {:<10}".format('Quality','MSE','RMSE','MAE'))

    for quality in classes:
        class_y = y[y == quality]
        class_y_pred = y_pred[y == quality]
        mse = metrics.mean_squared_error(class_y, class_y_pred)
        print("{:<10} {:<10.3f} {:<10.3f} {:<10.3f}".format(quality, mse, np.sqrt(mse), metrics.mean_absolute_error(class_y, class_y_pred)))

    #print("-------- REGRESSION TO CLASSIFICATION REPORT -------")
    #print(metrics.classification_report(y, np.round(y_pred)))
    print("----------------------------------------------------")

def print_classification_report(y, y_pred):
    print("------------------ OVERALL REPORT ------------------")
    print(metrics.classification_report(y, y_pred))
    print("----------------- CONFUSION MATRIX -----------------")
    print(pd.DataFrame(
        metrics.confusion_matrix(y, y_pred, labels=classes), 
        index=['true:'+str(i) for i in classes],
        columns=['pred:'+str(i) for i in classes]
    ))
    print("----------------------------------------------------")

def generate_report(y_test, y_pred, is_classification, time_elapsed):
    # Easier to just redirect stdout to a string instead of rewriting the functions
    from io import StringIO
    from contextlib import redirect_stdout

    with StringIO() as buf, redirect_stdout(buf):
        
        if (is_classification):
            print_classification_report(y_test, y_pred)
        else:
            print_regression_report(y_test, y_pred)

        formatted_time = time.strftime("%M:%S", time.gmtime(time_elapsed))
        print(f"Time elapsed: {formatted_time} ({time_elapsed} seconds)")
        report = buf.getvalue()
    
    return report

def save_model(model_name, model, report, scaler):
    import os
    import pickle
    folder_name = f'{models_folder}/{model_name}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
       
    with open(f'{folder_name}/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open(f'{folder_name}/report.txt', 'w') as f:
        f.write(report)
    with open(f'{folder_name}/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

def train_and_test(used_model_name):
    global x_train, y_train, x_test, y_test

    start_time = time.time()
    print("Training and testing model:", used_model_name + "...")

    # Normalize data
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    model = models[used_model_name]
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    time_elapsed = round(time.time() - start_time, 2)
    print("Done! Time elapsed: " + time.strftime("%M:%S", time.gmtime(time_elapsed)))

    report = generate_report(y_test, y_pred, is_classification = used_model_name.endswith('c'), time_elapsed = time_elapsed)
    save_model(used_model_name, model, report, scaler)
    #print(report)

train_and_test('svr.1_r')
train_and_test('svr1_r')
train_and_test('svr2_r')
train_and_test('svr10_r')
train_and_test('svr100_r')

