import pandas as pd
import time
import os

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

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor


dataset_folder = 'ml/datasets'
models_folder = 'ml/models'
reports_folder = 'ml/reports'
dataset_name = '6000x6-csrhn'

quality_mapping_6class = { 'FA': 1.0, 'GA': 0.9, 'B': 0.7, 'C': 0.6, 'Start': 0.4, 'Stub': 0.0 }
quality_mapping_5class = { 'FA': 1.0, 'GA': 1.0, 'B': 0.7, 'C': 0.6, 'Start': 0.4, 'Stub': 0.0 }
quality_mapping_3class = { 'FA': 1.0, 'GA': 1.0, 'B': 0.6, 'C': 0.6, 'Start': 0.0, 'Stub': 0.0 }
quality_mapping_2class = { 'FA': 1.0, 'GA': 1.0, 'B': 0.0, 'C': 0.0, 'Start': 0.0, 'Stub': 0.0 }

# Train and test models
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
    'logreg_c': LogisticRegression(max_iter=10000),

    'linreg_r': LinearRegression(),
    'tree_r': DecisionTreeRegressor(criterion='squared_error', random_state=0, max_depth=15),
    'forest_r': RandomForestRegressor(n_estimators=150, criterion='squared_error', random_state=0, max_depth=15),
    'ada_r': AdaBoostRegressor(n_estimators=150, random_state=0, learning_rate=0.1, base_estimator=DecisionTreeRegressor(max_depth=10)),
    'gboost_r': GradientBoostingRegressor(n_estimators=150, random_state=0, learning_rate=0.01),
    'svr_r': SVR(kernel='rbf', C=2, gamma='scale'), 
    'mlp_r': MLPRegressor(hidden_layer_sizes=(100,), max_iter=10000, alpha=0.1,), 
}

def load_dataset(class_mapping, feature_categories):
    train = pd.read_csv(f'{dataset_folder}/{dataset_name}_train.csv')
    test = pd.read_csv(f'{dataset_folder}/{dataset_name}_test.csv')

    x_train = train.drop(['Quality', 'Title'], axis=1)
    y_train = train['Quality'].replace(class_mapping)

    x_test = test.drop(['Quality', 'Title'], axis=1)
    y_test = test['Quality'].replace(class_mapping)

    x_train = x_train.filter(regex=f'^[{feature_categories}]', axis=1)
    x_test = x_test.filter(regex=f'^[{feature_categories}]', axis=1)

    return x_train, y_train, x_test, y_test, x_train.columns.tolist()

def print_regression_report(y, y_pred, classes):  
    print("------------------ OVERALL REPORT ------------------")
    print('Mean squared error (MSE): %.4f' % metrics.mean_squared_error(y, y_pred))
    print('Root mean squared error (RMSE): %.4f' % metrics.mean_squared_error(y, y_pred)**0.5)
    print('Mean absolute error (MAE): %.4f' % metrics.mean_absolute_error(y, y_pred))
    print('R2 score: %.4f' % metrics.r2_score(y, y_pred))

    print("----------------- PER-CLASS REPORT -----------------")
    print ("{:<10} {:<10} {:<10} {:<10}".format('Quality','MSE','RMSE','MAE'))

    for quality in classes:
        class_y = y[y == quality]
        class_y_pred = y_pred[y == quality]
        mse = metrics.mean_squared_error(class_y, class_y_pred)
        print("{:<10} {:<10.3f} {:<10.3f} {:<10.3f}".format(quality, mse, mse**0.5, metrics.mean_absolute_error(class_y, class_y_pred)))
    print("----------------------------------------------------")

def print_classification_report(y, y_pred, classes):
    print("------------------ OVERALL REPORT ------------------")
    print(metrics.classification_report(y, y_pred, labels=classes))
    print("----------------- CONFUSION MATRIX -----------------")
    print(pd.DataFrame(
        metrics.confusion_matrix(y, y_pred, labels=classes), 
        index=['true:'+str(i) for i in classes],
        columns=['pred:'+str(i) for i in classes]
    ))
    print("----------------------------------------------------")

def generate_report(y_test, y_pred, classes, is_classification, time_elapsed):
    # Easier to just redirect stdout to a string instead of rewriting the functions
    from io import StringIO
    from contextlib import redirect_stdout

    with StringIO() as buf, redirect_stdout(buf):
        
        if (is_classification):
            print_classification_report(y_test, y_pred, classes)
        else:
            print_regression_report(y_test, y_pred, classes)

        formatted_time = time.strftime("%M:%S", time.gmtime(time_elapsed))
        print(f"Time elapsed: {formatted_time} ({time_elapsed} seconds)")
        report = buf.getvalue()
    
    return report

def save_model(model_path, model, report, scaler, features):
    import pickle

    if not os.path.exists(model_path):
        os.makedirs(model_path)
       
    with open(f'{model_path}/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open(f'{model_path}/report.txt', 'w') as f:
        f.write(report)
    with open(f'{model_path}/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open(f'{model_path}/features.pkl', 'wb') as f:
        pickle.dump(features, f)
    

def save_report(report_path, report):
    if not os.path.exists(os.path.dirname(report_path)):
        os.makedirs(os.path.dirname(report_path))

    with open(report_path, 'w') as f:
        f.write(report)

def train_and_test(model_name, class_mapping, feature_categories, do_save_model = False):    
    start_time = time.time()

    is_classification = model_name.endswith('c')

    if (is_classification): 
        new_class_mapping = {}
        for key, label in class_mapping.items():
            keys = [k for k, v in class_mapping.items() if v == label] # get all keys with label as value             
            new_class_mapping[key] = '.'.join(keys) # concatenate all elements of keys
        class_mapping = new_class_mapping

    
    x_train, y_train, x_test, y_test, features = load_dataset(class_mapping, feature_categories)
    classes = list(dict.fromkeys(class_mapping.values())) # remove duplicates whilst preserving order (https://stackoverflow.com/a/17016257)
    
    print(f"Training and testing model: {model_name}")
    print(f"Training with categories {feature_categories} ({len(x_train.columns)} features) and {len(classes)} classes")

    # Normalize data
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)


    model = models[model_name]
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    
    time_elapsed = round(time.time() - start_time, 2)
    print("Done! Time elapsed: " + time.strftime("%M:%S", time.gmtime(time_elapsed)))

    report = generate_report(y_test, y_pred, classes, is_classification = is_classification, time_elapsed = time_elapsed)

    if do_save_model:
        model_path = f'{models_folder}/{feature_categories + str(len(classes))}/{model_name}'
        save_model(model_path, model, report, scaler, features)
    else: 
        report_path = f'{reports_folder}/{feature_categories + str(len(classes))}/{model_name}.report.txt'
        save_report(report_path, report)
    
    return model, report

def perform_mass_training():
    for modelname in models:
        train_and_test(modelname, quality_mapping_6class, "CSRHN") # Default

        train_and_test(modelname, quality_mapping_5class, "CSRHN")
        train_and_test(modelname, quality_mapping_3class, "CSRHN")
        train_and_test(modelname, quality_mapping_2class, "CSRHN")

        train_and_test(modelname, quality_mapping_6class, "SRHN")
        train_and_test(modelname, quality_mapping_6class, "CRHN")
        train_and_test(modelname, quality_mapping_6class, "CSHN")
        train_and_test(modelname, quality_mapping_6class, "CSRN")
        train_and_test(modelname, quality_mapping_6class, "CSRH")

        train_and_test(modelname, quality_mapping_6class, "C")
        train_and_test(modelname, quality_mapping_6class, "S")
        train_and_test(modelname, quality_mapping_6class, "R")
        train_and_test(modelname, quality_mapping_6class, "H")
        train_and_test(modelname, quality_mapping_6class, "N")

        train_and_test(modelname, quality_mapping_6class, "CSR")
        train_and_test(modelname, quality_mapping_6class, "CSH")
        train_and_test(modelname, quality_mapping_6class, "CRH")
        train_and_test(modelname, quality_mapping_6class, "CH")


#model, report = train_and_test('forest_r', quality_mapping_6class, "CRH", do_save_model = True)

perform_mass_training()

    

    