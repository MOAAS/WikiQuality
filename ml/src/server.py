from flask import Flask
from flask_cors import CORS

import wikiapi
import pickle
from features.main import compute_features, features_to_dataframe
from wikitext_cleaner import clean_wikitext


# Load model
model_folder = '../models'
model_name = 'linreg'
with open(f'{model_folder}/{model_name}.pkl', 'rb') as f:
    model = pickle.load(f)

# Create Flask App
app = Flask(__name__)
CORS(app) # CORS: Allow all

@app.route("/evaluate/<title>")
def evaluate(title):    
    # todo: validate if page exists

    wikitext = wikiapi.getWikiText(title)
    features = compute_features(title, wikitext)
    features_df = features_to_dataframe(features)
    quality = model.predict(features_df)[0]

    return {"title": title, "quality": str(quality), "zfeatures": features}

@app.route("/features/<title>")
def features(title):
    wikitext = wikiapi.getWikiText(title)
    features = compute_features(title, wikitext)

    return {"title": title, **features}
    

@app.route("/plain/<title>")
def plain(title):
    wikitext = wikiapi.getWikiText(title)
    plaintext = clean_wikitext(wikitext, title)
    return "<pre>" + plaintext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + "</pre>"

@app.route("/wikitext/<title>")
def wikitext(title):
    wikitext = wikiapi.getWikiText(title)
    return "<pre>" + wikitext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + "</pre>"
