import pandas as pd
from wikitext_cleaner import clean_wikitext
from features.content import compute_content_features, CONTENT_FEATURES
from features.style import compute_style_features, STYLE_FEATURES
from features.readability import compute_readability_features, READABILITY_FEATURES
from features.network import compute_network_features, NETWORK_FEATURES
from features.history import compute_history_features, HISTORY_FEATURES

from features.text_analysis import compute_words, compute_sentences, estimate_syllables


# Some features may be calculated using specific api calls (e.g. query -> contributors)
# Note: ML Model will not go on the frontend, so might as well ask server (python) to compute features

def features_to_dataframe(feature_list):
    # FEATURE_HEADERS without title or quality
    columns = FEATURE_HEADERS[1:]
    columns = columns[:-1]   
    
    return pd.DataFrame([feature_list], columns=columns)

def compute_features(title, wikitext):
    plaintext = clean_wikitext(wikitext, title)

    if len(plaintext) == 0:
        print("Found empty text for: " + title)
        plaintext = 'This page is empty.'

    # did this here to improve performance: compute_sentences and compute_words are slow. 
    # estimate_syllables not so much but keep for consistency + it helps
    sentences = compute_sentences(plaintext)
    sentence_words = [compute_words(sentence) for sentence in sentences]
    words = [word for sentence in sentence_words for word in sentence]
    sentence_word_lengths = [len(sentence) for sentence in sentence_words]
    syllables = [estimate_syllables(word) for word in words]


    content = compute_content_features(wikitext, plaintext)
    style = compute_style_features(sentences, words, syllables, sentence_word_lengths)
    readability = compute_readability_features(sentences, words, syllables)
    network = compute_network_features(wikitext, plaintext)
    history = compute_history_features(wikitext, plaintext)
  
    return { "title": title, **content, **style, **readability, **network, **history }


FEATURE_HEADERS = ['Title'] + CONTENT_FEATURES + STYLE_FEATURES + READABILITY_FEATURES + HISTORY_FEATURES + NETWORK_FEATURES + ['Quality']
