from operator import ge
from traceback import print_tb
import requests

import os
import sys # https://stackoverflow.com/a/11158224 allow for parent imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import wikiapi

import re
import pandas as pd
from helpers import load_model
from features.main import compute_features

quality_translations = {
    'standard': ['A+', 'A', 'B', 'C', 'D', 'F'],
    'en': ['fa', 'ga', 'b', 'c', 'start', 'stub'], # https://en.wikipedia.org/wiki/Wikipedia:Content_assessment
    'fr': ['adq', 'ba', 'a', 'b', 'bd', 'ébauche'], # https://fr.wikipedia.org/wiki/Projet:%C3%89valuation/Avancement
    'pt': ['6', '5', '4', '3', '2', '1'], # https://pt.wikipedia.org/wiki/Predefini%C3%A7%C3%A3o:Escala_de_avalia%C3%A7%C3%A3o
    'ru': ['ис', 'хс', 'i', 'ii', 'iii', 'iv'] # https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82:%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F/%D0%9E%D1%86%D0%B5%D0%BD%D0%BA%D0%B8
}

quality_mapping = { 'A+': 1.0, 'A': 0.9, 'B': 0.7, 'C': 0.6, 'D': 0.4, 'F': 0.0 }

def extract_quality(language, talk):
    lang_map = dict(zip(quality_translations[language], quality_translations['standard']))
    
    if (language == 'en'):
        matches = re.findall(r'{{(.*?)class=(.*?)[|\n}]', talk, re.DOTALL | re.IGNORECASE)
        qualities = [match[1] for match in matches]
    elif (language == 'fr'):
        matches = re.findall(r'{{(.*?)avancement=(.*?)[|\n}]', talk, re.DOTALL | re.IGNORECASE)
        qualities = [match[1] for match in matches]
    elif (language == 'pt'):
        matches = re.findall(r'{{marca de projeto\|(.*?)\|', talk, re.DOTALL | re.IGNORECASE)
        qualities = [match for match in matches]
    elif (language == 'ru'):
        matches = re.findall(r'{{(.*?)уровень=(.*?)[|\n}]', talk, re.DOTALL | re.IGNORECASE)
        qualities = [match[1] for match in matches]
    else:
        return None

    valid_qualities = lang_map.keys()
    qualities = [quality.strip().lower() for quality in qualities]
    qualities = [quality for quality in qualities if quality in valid_qualities]

    if len(qualities) == 0:
        return None
    quality = max(set(qualities), key=qualities.count) # get most common
    return lang_map[quality]

dataset_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets')

def generate_multilanguage_dataset(language, num_articles):

    dataset_name = f'multi-{language}-{num_articles}-csrh.csv'
    dataset = []

    wikiapi.updateLanguage(language)
    titles = wikiapi.getRandomArticles(num_articles, forceTalk=True)
    wikitexts = wikiapi.getMultiWikiText(titles) # Collect wikitexts
    talks = wikiapi.getMultiWikiText(['Talk:' + title for title in titles]) # Collect talk wikitexts    
    talks = {key.split(':', 1)[1]: value for key, value in talks.items()} # remove Talk: from every key

    for i, title in enumerate(titles):
        if (i % 100 == 0):
            print(f'Analyzing {num_articles} articles... {i}/{len(titles)}')

        if (title not in wikitexts or title not in talks):
            continue       
        
        quality = extract_quality(language, talks[title]) # Check quality
        if (quality is None):
            continue

        features = {
            "Title": title.replace('"', '').replace(',', ' '), # avoid CSV problems (not used anyway)
            **compute_features(title, wikitexts[title]),
            "Quality": quality,
        }

        dataset.append(features)

    print(f'Analyzing {num_articles} articles... {len(dataset)}/{len(titles)}')  

    df = pd.DataFrame(dataset)
    df.to_csv(os.path.join(dataset_folder, dataset_name), index=False)
    
    
def evaluate_dataset(dataset_name):
    features = "CRH"
    model, _, scaler = load_model(f'{features}6/forest_r')

    # load dataset
    df = pd.read_csv(os.path.join(dataset_folder, dataset_name))
    x = df.drop(columns=['Title', 'Quality'], axis=1)
    x = x.filter(regex=f'^[{features}]', axis=1)  
    x = scaler.transform(x)
    y = df['Quality'].apply(lambda x: quality_mapping[x])
    y_pred = model.predict(x)

    # print regression metrics
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    print("----- " + dataset_name + " -----")
    print('Mean squared error (MSE): %.4f' % mean_squared_error(y, y_pred))
    print('Root mean squared error (RMSE): %.4f' % mean_squared_error(y, y_pred) ** 0.5)
    print('Mean absolute error (MAE): %.4f' % mean_absolute_error(y, y_pred))


#generate_multilanguage_dataset('en', 6000)
#generate_multilanguage_dataset('fr', 6000)
#generate_multilanguage_dataset('pt', 12000)
#generate_multilanguage_dataset('ru', 12000)

evaluate_dataset('6000-csrh-multi-en.csv')
evaluate_dataset('6000-csrh-multi-fr.csv')
evaluate_dataset('12000-csrh-multi-pt.csv')
evaluate_dataset('12000-csrh-multi-ru.csv')
