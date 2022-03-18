import random

from fileinput import filename
from matplotlib.pyplot import title
from features import FEATURE_HEADERS, compute_features

partition = {
    'FA': 40,
    'FL': 0,
    'A': 40,
    'GA': 40,
    'B': 40,
    'C': 40,
    'Start': 40,
    'Stub': 40,   
}

train = []
test = []

# Collect random titles from each file
for quality in partition:
    filename = f'titles/{quality}.txt'
    print(f'Collecting {partition[quality]} random titles from {filename}')
    with open(filename, 'r', encoding='utf-8') as f:
        titles = f.read().split('\n')
        random.shuffle(titles)
        titles = titles[:partition[quality]]
        
    # 70% to train.csv 30% to test.csv
    for i, title in enumerate(titles):
        if i < partition[quality] * 0.7:
            train.append(compute_features(title) + [quality])
        else:
            test.append(compute_features(title) + [quality])

        
# open train.csv and test.csv and write to them
with open('datasets/train.csv', 'w', encoding='utf-8') as ftrain, open('datasets/test.csv', 'w', encoding='utf-8') as ftest:
    ftrain.write(','.join(FEATURE_HEADERS) + '\n')   
    ftest.write(','.join(FEATURE_HEADERS) + '\n')

    for row in train:        
        ftrain.write(','.join(str(x) for x in row) + '\n')

    for row in test:    
        ftest.write(','.join(str(x) for x in row) + '\n')


