from flask import Flask
from flask_cors import CORS

import wikiapi
import pickle
import os
from features.main import compute_features, features_to_dataframe
from wikitext_cleaner import clean_wikitext

# TODO: Titles with slashes must work: E.g (Fences/Mansions_Split_7") 

# Load model
model_folder = os.path.join(os.path.dirname(__file__), '..', 'models', 'CSRH6')
model_name = 'forest_r'
with open(f'{model_folder}/{model_name}/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open(f'{model_folder}/{model_name}/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Create Flask App
app = Flask(__name__)
CORS(app) # CORS: Allow all

@app.route("/evaluate/<title>")
@app.route("/evaluate/<title>/<language>")
def evaluate(title, language='en'):    
    # todo: validate if page exists

    wikiapi.updateLanguage(language)
    wikitext = wikiapi.getWikiText(title)
    num_translations = wikiapi.getSingleNumTranslations(title)
    features = compute_features(title, wikitext, num_translations)
    wikiapi.resetLanguage()

    features_df = features_to_dataframe(features)
    features_df = scaler.transform(features_df)
    quality = model.predict(features_df)[0]

    return {"title": title, "quality": str(quality), "zfeatures": features}

@app.route("/features/<title>")
def features(title):
    wikitext = wikiapi.getWikiText(title)
    num_translations = wikiapi.getSingleNumTranslations(title)
    features = compute_features(title, wikitext, num_translations)

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

@app.route("/history/<title>")
def history(title):
    history = wikiapi.getFullHistory(title)

    return { "history": history }
