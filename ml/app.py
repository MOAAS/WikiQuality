from flask import Flask
from flask_cors import CORS

from features import compute_features, features_to_dataframe
import pandas as pd

# load model from pickle
import pickle
with open('models/decision_tree.pkl', 'rb') as f:
    model = pickle.load(f)




app = Flask(__name__)
CORS(app) # cors allow all

@app.route("/evaluate/<title>")
def hello_name(title):    
    # todo: validate if page exists
    features = compute_features(title)
    features = features_to_dataframe(features)
    quality = model.predict(features)[0]
    
    return {"title": title, "quality": quality}
