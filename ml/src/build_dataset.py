import random
import wikiapi
import time

from fileinput import filename
from matplotlib.pyplot import title
from features.main import FEATURE_HEADERS, compute_features, clean_wikitext

partition = {
    'FA': 40,   
    'FL': 0,     
    'A': 0,    
    'GA': 40,   
    'B': 40,    
    'C': 40,     
    'Start': 40,
    'Stub': 40, 
}

quality_values = { 'FA': 5, 'FL': 5, 'A': 5, 'GA': 4, 'B': 3, 'C': 2, 'Start': 1, 'Stub': 0 }

train = []
test = []

build_regression_dataset = True

titles_folder = 'ml/titles'
datasets_folder = 'ml/datasets'
error_folder = 'ml/src'

start_time = time.time()

for quality in partition:
    filename = f'{titles_folder}/{quality}.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        # Collect random titles from each file
        print(f'Collecting {partition[quality]} random titles from {filename}')
        titles = f.read().split('\n')
        random.shuffle(titles)
        titles = titles[:partition[quality]]

        # Collect wikitexts
        wikitexts = wikiapi.getMultiWikiText(titles)
                
    # 70% to train.csv 30% to test.csv
    for i, title in enumerate(titles):
        try:
            if i % 50 == 0:
                print(f'Computing features of {len(titles)} pages... {i}/{len(titles)}')

            # if title is not in wikitexts
            if title not in wikitexts:
                print(f'Page {title} was missing, not adding to dataset.')
                continue

            wikitext = wikitexts[title]
            
            features = {
                "Title": title,
                "Quality": quality_values[quality] if build_regression_dataset else quality,
                **compute_features(title, wikitext)
            }
        except Exception as e:
            with open(f'{error_folder}/ERROR-BUILD-DATASET.txt', 'w', encoding='utf-8') as f:
                print("Error on title: " + title + "... Writing to log file")
                f.write("ERROR BUILDING DATASET\n\n TITLE: " + title + "\n\n")
                f.write('URL: https://en.wikipedia.org/wiki/' + title.replace(' ', '_') + '\n\n')
                f.write("======================= ========== =======================\n")
                f.write("==================== ORIGINAL WIKITEXT ===================\n")
                f.write("======================= ========== =======================\n")
                wikitext = wikiapi.getWikiText(title)
                f.write(wikitext + "\n\n")
                f.write("======================= ========== ==========================\n")
                f.write("======================= PLAIN TEXT ==========================\n")
                f.write("======================= ========== ==========================\n")
                f.write(clean_wikitext(wikitext, title))                
            raise

        if i < partition[quality] * 0.7:
            train.append(features)
        else:
            test.append(features)

def write_features(dataset, file):
    for dict in dataset:
        line = ','.join(['"' + str(dict[key]) + '"' for key in FEATURE_HEADERS])
        file.write(line + '\n')
                
        missing_features = set(FEATURE_HEADERS) - set(dict.keys())
        if missing_features:
            print(f'Missing features: {missing_features} (dict{str(dict)})')
            raise Exception('Missing features')

# open train.csv and test.csv and write to them
with open(f'{datasets_folder}/train.csv', 'w', encoding='utf-8') as ftrain, open(f'{datasets_folder}/test.csv', 'w', encoding='utf-8') as ftest:
    ftrain.write(','.join(FEATURE_HEADERS) + '\n')   
    ftest.write(','.join(FEATURE_HEADERS) + '\n')

    write_features(train, ftrain)
    write_features(test, ftest)    

end_time = time.time()
print(f'Dataset built. Time elapsed: {round(end_time - start_time, 2)} seconds.')
