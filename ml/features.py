import wikiapi
import pandas as pd

FEATURE_HEADERS = ["Title Length", "Text Length", "Quality"]

# Some features may be calculated using specific api calls (e.g. query -> contributors)
# Note: ML Model will not go on the frontend, so might as well ask server (python) to compute features

def compute_features(title):
    
    return [len(title), len(wikiapi.getWikiPageText(title))]

def features_to_dataframe(feature_list):
    return pd.DataFrame([feature_list], columns=FEATURE_HEADERS[:-1])