from flask import Flask
from flask_cors import CORS

from features import compute_features, features_to_dataframe
import pandas as pd
import wikiapi
from wikitext_cleaner import clean_wikitext


# load model from pickle
import pickle
with open('models/decision_tree.pkl', 'rb') as f:
    model = pickle.load(f)




app = Flask(__name__)
CORS(app) # cors allow all

@app.route("/evaluate/<title>")
def evaluate(title):    
    # todo: validate if page exists

    wikitext = wikiapi.getWikiText(title)
    features = compute_features(title, wikitext)
    features = features_to_dataframe(features)
    quality = model.predict(features)[0]    
    
    return {"title": title, "quality": quality}

@app.route("/features/<title>")
def features(title):
    wikitext = wikiapi.getWikiText(title)
    features = compute_features(title, wikitext)

    return {"title": title, **features}
    

@app.route("/plain/<title>")
def plain(title):
    wikitext = wikiapi.getWikiText(title)
    plaintext = clean_wikitext(wikitext, title, writeToFile=False)
    return "<pre>" + plaintext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + "</pre>"

@app.route("/wikitext/<title>")
def wikitext(title):
    wikitext = wikiapi.getWikiText(title)
    return "<pre>" + wikitext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + "</pre>"

@app.route("/test")
def test():
    return []
