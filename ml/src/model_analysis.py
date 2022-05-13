import matplotlib.pyplot as plot
import pickle
import os



def load_model(modelname):
    model_folder = os.path.join(os.path.dirname(__file__), '..', 'models')

    with open(f'{model_folder}/{modelname}/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(f'{model_folder}/{modelname}/features.pkl', 'rb') as f:
        features = pickle.load(f)

    return model, features

def analyze_feature_importance(modelname):
    # load model from pickle
    model, features = load_model(modelname)
    importance = model.feature_importances_

    # make dictonary of feature names and importance values
    feature_importance = dict(zip(features, importance))

    # get the top 10 and bottom 10 features
    top_10 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15])
    bottom_10 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)[:15])
    
    figure, axis = plot.subplots(2, 1)

    axis[0].bar(top_10.keys(), top_10.values())
    axis[0].set_title('Feature Importance: Top 10')

    axis[1].bar(bottom_10.keys(), bottom_10.values())
    axis[1].set_title('Feature Importance: Bottom 10')

    figure.tight_layout()

    plot.show()



analyze_feature_importance("CSRH6/forest_r")
