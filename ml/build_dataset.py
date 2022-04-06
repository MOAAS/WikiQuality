import random
import wikiapi

from fileinput import filename
from matplotlib.pyplot import title
from features import FEATURE_HEADERS, compute_features, clean_wikitext

partition = {
    'FA': 4000,   
    'FL': 0,     
    'A': 750,    
    'GA': 4000,   
    'B': 4000,    
    'C': 4000,     
    'Start': 4000,
    'Stub': 4000, 
}

quality_values = { 'FA': 6, 'FL': 6, 'A': 5, 'GA': 4, 'B': 3, 'C': 2, 'Start': 1, 'Stub': 0 }

train = []
test = []

build_regression_dataset = True

for quality in partition:
    filename = f'ml/titles/{quality}.txt'
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
            wikitext = wikitexts[title]
            if wikitext is None:
                print(f'({title}) is missing... skipping this page.')
                continue
            features = {
                "Title": title,
                "Quality": quality_values[quality] if build_regression_dataset else quality,
                **compute_features(title, wikitext)
            }
        except Exception as e:
            with open(f'ml/log/ERROR-BUILD-DATASET.txt', 'w', encoding='utf-8') as f:
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
datasets_folder = 'ml/datasets'
with open(datasets_folder + '/train.csv', 'w', encoding='utf-8') as ftrain, open(datasets_folder + '/test.csv', 'w', encoding='utf-8') as ftest:
    ftrain.write(','.join(FEATURE_HEADERS) + '\n')   
    ftest.write(','.join(FEATURE_HEADERS) + '\n')

    write_features(train, ftrain)
    write_features(test, ftest)    

