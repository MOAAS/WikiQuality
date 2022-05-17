import requests

import os
import sys # https://stackoverflow.com/a/11158224 allow for parent imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import wikiapi

import re
from helpers import load_model

quality_mapping = { 'FA': 1.0, 'GA': 0.9, 'B': 0.7, 'C': 0.6, 'Start': 0.4, 'Stub': 0.0 }

def extract_quality(language, talk):
    if language == 'en':
        matches = re.findall(r'{{(.*?)class=(.*?)[|\n}]', talk, re.DOTALL | re.IGNORECASE)
        qualities = [match[1].strip().lower() for match in matches]
        valid_qualities = ['fa', 'ga', 'b', 'c', 'start', 'stub']
        qualities = [quality for quality in qualities if quality in valid_qualities]
        
        if len(qualities) == 0:
            return None
        quality = max(set(qualities), key=qualities.count) # get most common
        return quality
    else:
        return 'B'

def get_random_article(language):
    req = requests.get(f'https://{language}.wikipedia.org/wiki/Special:Random')
    url = req.url
    title = url.split('/wiki/')[1]
    return title

def get_random_and_extract(language):
    title = get_random_article(language)

    while True:
        print(title)
        try:
            wikitext = wikiapi.getWikiText(title)
            talk = wikiapi.getWikiText('Talk:' + title)
            quality = extract_quality(language, talk)
            if (quality is None):
                raise Exception('No quality')
            break
        except:
            title = get_random_article(language)
            continue

    #print(talk[:200])
    #print(quality)
    return title, quality, wikitext



def evaluate_multilingual():
    model, features = load_model('CSRH6/forest_r')

    y = []
    y_pred = []

    title, quality, wikitext = get_random_and_extract('en')




evaluate_multilingual()
