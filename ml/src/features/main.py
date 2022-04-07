import pandas as pd
import re
from wikitext_cleaner import clean_wikitext
from features.content import compute_content_features, CONTENT_FEATURES
from features.style import compute_style_features, STYLE_FEATURES
from features.readability import compute_readability_features, READABILITY_FEATURES
from features.network import compute_network_features, NETWORK_FEATURES
from features.history import compute_history_features, HISTORY_FEATURES



# Some features may be calculated using specific api calls (e.g. query -> contributors)
# Note: ML Model will not go on the frontend, so might as well ask server (python) to compute features

def features_to_dataframe(feature_list):
    # FEATURE_HEADERS without title or quality
    columns = FEATURE_HEADERS[1:]
    columns = columns[:-1]   
    
    return pd.DataFrame([feature_list], columns=columns)

def compute_features(title, wikitext):
    plaintext = clean_wikitext(wikitext, title)

    content = compute_content_features(wikitext, plaintext)
    style = compute_style_features(wikitext, plaintext)
    readability = compute_readability_features(wikitext, plaintext)
    network = compute_network_features(wikitext, plaintext)
    history = compute_history_features(wikitext, plaintext)
  
    return { "title": title, **content, **style, **readability, **network, **history }


FEATURE_HEADERS = ['Title'] + CONTENT_FEATURES + STYLE_FEATURES + READABILITY_FEATURES + HISTORY_FEATURES + NETWORK_FEATURES + ['Quality']
