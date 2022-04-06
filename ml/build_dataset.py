import random
import wikiapi

from fileinput import filename
from matplotlib.pyplot import title
from features import FEATURE_HEADERS, compute_features, clean_wikitext

partition = {
    'FA': 400,
    'FL': 0,
    'A': 400,
    'GA': 400,
    'B': 400,
    'C': 400,
    'Start': 400,
    'Stub': 400,   
}

train = []
test = []

# Collect random titles from each file
for quality in partition:
    filename = f'ml/titles/{quality}.txt'
    print(f'Collecting {partition[quality]} random titles from {filename}')
    with open(filename, 'r', encoding='utf-8') as f:
        titles = f.read().split('\n')
        random.shuffle(titles)
        titles = titles[:partition[quality]]

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
                "Quality": quality,
                **compute_features(title, wikitext)
            }
        except Exception as e:
            with open(f'ml/log/ERROR-BUILD-DATASET.txt', 'w', encoding='utf-8') as f:
                print("Error on title: " + title + "... Writing to log file")
                print(wikitexts[title])
                f.write("ERROR BUILDING DATASET\n\n")
                f.write("TITLE: ")
                f.write(title)
                f.write('\n\nURL: https://en.wikipedia.org/wiki/' + title.replace(' ', '_') + '\n\n')
                f.write("======================= ========== =======================\n")
                f.write("==================== ORIGINAL WIKITEXT ===================\n")
                f.write("======================= ========== =======================\n")
                wikitext = wikiapi.getWikiText(title)
                f.write(wikitext)
                f.write("\n\n")
                f.write("======================= ========== ==========================\n")
                f.write("======================= PLAIN TEXT ==========================\n")
                f.write("======================= ========== ==========================\n")
                plaintext = clean_wikitext(wikitext, title, writeToFile=False)
                f.write(plaintext)
                
            raise

        if i < partition[quality] * 0.7:
            train.append(features)
        else:
            test.append(features)

# open train.csv and test.csv and write to them
with open('ml/datasets/train.csv', 'w', encoding='utf-8') as ftrain, open('ml/datasets/test.csv', 'w', encoding='utf-8') as ftest:

    ftrain.write(','.join(FEATURE_HEADERS) + '\n')   
    ftest.write(','.join(FEATURE_HEADERS) + '\n')

    def write_features(dataset, file):
        for dict in dataset:
            line = ','.join(['"' + str(dict[key]) + '"' for key in FEATURE_HEADERS])
            file.write(line + '\n')
                    
            missing_features = set(FEATURE_HEADERS) - set(dict.keys())
            if missing_features:
                print(f'Missing features: {missing_features} (dict{str(dict)})')
                raise Exception('Missing features')

    write_features(train, ftrain)
    write_features(test, ftest)    


