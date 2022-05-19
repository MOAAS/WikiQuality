import pandas as pd
import wikiapi

from wikitext_cleaner import clean_wikitext
from features.content import compute_content_features
from features.style import compute_style_features
from features.readability import compute_readability_features
from features.network import compute_network_features
from features.history import compute_history_features

from features.text_analysis import compute_words, compute_sentences, estimate_syllables

def features_to_dataframe(features):    
    return pd.DataFrame([features], columns=features.keys())

def compute_features(title, wikitext, num_translations = 0, graph_info = None):
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
    revisions = wikiapi.getFullHistory(title)

    content = compute_content_features(wikitext, plaintext, words, sentences)
    style = compute_style_features(sentences, words, syllables, sentence_word_lengths)
    readability = compute_readability_features(sentences, words, syllables)
    history = compute_history_features(revisions)
    network = compute_network_features(title, num_translations, graph_info)
  
    return { **content, **style, **readability, **history, **network }

