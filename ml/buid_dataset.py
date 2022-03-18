from fileinput import filename

from matplotlib.pyplot import title
import wikiapi
import random

partition = {
    'FA': 4000,
    'FL': 0,
    'A': 4000,
    'GA': 4000,
    'B': 4000,
    'C': 4000,
    'Start': 4000,
    'Stub': 4000,   
}



# open train.csv and test.csv
with open('datasets/train.csv', 'w', encoding='utf-8') as ftrain, open('datasets/test.csv', 'w', encoding='utf-8') as ftest:
    ftrain.write('Title,Category\n')
    ftest.write('Title,Category\n')

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
                ftrain.write(f'{title},{quality}\n')
            else:
                ftest.write(f'{title},{quality}\n')

        
        
