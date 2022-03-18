from flask import Flask
from features import compute_features, features_to_dataframe
import pandas as pd

# load model from pickle
import pickle
with open('models/decision_tree.pkl', 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)

@app.route("/evaluate/<title>")
def hello_name(title):    
    features = compute_features(title)
    features = features_to_dataframe(features)

    quality = model.predict(features)[0]
    
    return {"title": title, "quality": quality}
