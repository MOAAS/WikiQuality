import random
import wikiapi
import time
import os

from features.main import compute_features
from features.graph_builder import build_graph

partition = {
    'FA': 6000,   
    'FL': 0,     
    'A': 0,    
    'GA': 6000,   
    'B': 6000,    
    'C': 6000,     
    'Start': 6000,
    'Stub': 6000, 
}


train = []
test = []

build_network_features = True

datasets_folder = 'ml/datasets'
dataset_name = '6000x6-csrhn'

start_time = time.time()

def collect_random_titles(quality, amount):
    with open(os.path.join(os.path.dirname(__file__), '..', 'titles', quality + ".txt"), 'r', encoding='utf-8') as f:
        titles = f.read().split('\n')
        random.shuffle(titles)
        titles = titles[:amount]
        return titles

for quality in partition:
    print(f'Collecting {partition[quality]} random {quality} titles')
    titles = collect_random_titles(quality, partition[quality])
        
    wikitexts = wikiapi.getMultiWikiText(titles) # Collect wikitexts        
    titles = list(wikitexts.keys()) # Update wrongly formatted titles
    translations = wikiapi.getNumTranslations(titles) # Collect translations

    if build_network_features:  
        graph_info = build_graph(titles) # Build graph (in-degree's, out-degree's and neighbors)
        titles = list(graph_info[2].keys()) # remove titles not present in graph_ids (third element)
    else:
        graph_info = None
            
    # 70% to train.csv 30% to test.csv
    for i, title in enumerate(titles):
        try:
            if i % 100 == 0:
                print(f'Computing features of {len(titles)} pages... {i}/{len(titles)}')

            # if title is not in wikitexts
            if title not in wikitexts:
                print(f'Page {title} was missing, not adding to dataset.')
                continue

            wikitext = wikitexts[title]
            
            features = {
                "Title": title.replace('"', '').replace(',', ' '), # we do this replace to avoid problems with the CSV. it's not an issue because titles are not used in the model
                **compute_features(title, wikitext, translations[title], graph_info),
                "Quality": quality,
            }
        except Exception as e:
            raise Exception(f'Error computing features of {title}!' + str(e))

        if i < len(titles) * 0.7:
            train.append(features)
        else:
            test.append(features)
    
    print(f'Computing features of {len(titles)} pages... {len(titles)}/{len(titles)}')

feature_names = list(train[0].keys())

def write_features(dataset, file):
    for feature in dataset:
        line = ','.join(['"' + str(feature[key]) + '"' for key in feature_names])
        file.write(line + '\n')
                
        missing_features = set(feature_names) - set(feature.keys())
        extra_features = set(feature.keys()) - set(feature_names)
        if len(missing_features) > 0 or len(extra_features) > 0:
            print(f'Missing features: {missing_features} (row: {str(feature)})')
            print(f'Extra features: {extra_features} (row: {str(feature)})')
            raise Exception('Missing features')

# open train.csv and test.csv and write to them
with open(f'{datasets_folder}/{dataset_name}_train.csv', 'w', encoding='utf-8') as ftrain, open(f'{datasets_folder}/{dataset_name}_test.csv', 'w', encoding='utf-8') as ftest:
    ftrain.write(','.join(feature_names) + '\n')   
    ftest.write(','.join(feature_names) + '\n')

    write_features(train, ftrain)
    write_features(test, ftest)    

end_time = time.time()
print(f'Dataset built. Time elapsed: {round(end_time - start_time, 2)} seconds. Number of features: {len(feature_names)}')
