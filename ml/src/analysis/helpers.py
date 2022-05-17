import os
import pickle

model_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'models')

def load_model(modelname):
    with open(f'{model_folder}/{modelname}/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(f'{model_folder}/{modelname}/features.pkl', 'rb') as f:
        features = pickle.load(f)

    return model, features