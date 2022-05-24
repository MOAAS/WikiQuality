import time
import matplotlib.pyplot as plot
import os
import random

import sys # https://stackoverflow.com/a/11158224 allow for parent imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import wikiapi

from features.main import compute_features

titles_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'titles')
report_times_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'times')

def collect_random_titles(quality, amount):
    with open(os.path.join(titles_folder, quality + ".txt"), 'r', encoding='utf-8') as f:
        titles = f.read().split('\n')
        random.shuffle(titles)
        titles = titles[:amount]
        return titles

def load_times(quality, type):
    with open(os.path.join(report_times_folder, quality, type + '.txt'), 'r', encoding='utf-8') as f:
        times = f.read().strip().split('\n')
        times = [float(time) for time in times]
        return times

# compute features does not compute times currently (too messy)
# if you need to run this again, change compute_features
def fetch_computation_times():
    # delete report_times_folder
    if os.path.exists(report_times_folder):
        for f in os.listdir(report_times_folder):
            os.remove(os.path.join(report_times_folder, f))
    # now remake it
    if not os.path.exists(report_times_folder):
        os.makedirs(report_times_folder)

    # load FA titles
    partition = { 'FA': 500, 'GA': 500, 'B': 500, 'C': 500, 'Start': 500, 'Stub': 500 }

    for quality in partition:
        print("Measuring " + quality + " articles...")
        titles = collect_random_titles(quality, partition[quality])

        # make folder
        if not os.path.exists(os.path.join(report_times_folder, quality)):
            os.makedirs(os.path.join(report_times_folder, quality))

        for title in titles:
            start = time.time()
            wikitext = wikiapi.getWikiText(title)
            if wikitext == '':
                continue           

            wikitext_elapsed = time.time() - start
            
            feats = compute_features(title, wikitext)
            (clean_wiki, tokenizer, syllables, revs, content, style, readability, history) = feats['times'] 

            def write_time(name, time):
                with open(os.path.join(report_times_folder, quality, name + '.txt'), 'a', encoding='utf-8') as f:
                    f.write(str(time) + "\n")
            
            write_time('wikitext', wikitext_elapsed)
            write_time('clean_wiki', clean_wiki)
            write_time('tokenizer', tokenizer)
            write_time('syllables', syllables)
            write_time('revs', revs)
            write_time('content', content)
            write_time('style', style)
            write_time('readability', readability)
            write_time('history', history)
            write_time('total', wikitext_elapsed + clean_wiki + tokenizer + syllables + revs + content + style + readability + history)
            
        with open(os.path.join(report_times_folder, quality, 'titles.txt'), 'a', encoding='utf-8') as f:
            f.write('\n'.join(titles))

def analyze_computation_times():
    print("{:<12}{:<7}{:<7}{:<7}{:<7}{:<7}{:<7}".format('Task','FA', 'GA', 'B', 'C', 'Start', 'Stub'))
    for task in ['wikitext', 'clean_wiki', 'tokenizer', 'syllables', 'revs', 'content', 'style', 'readability', 'history', 'total']:
        means = []
        for quality in ['FA', 'GA', 'B', 'C', 'Start', 'Stub']:
            times = load_times(quality, task)
            mean = sum(times) / len(times)
            means.append(mean)
            
        # print all means rounded to 3 decimal places
        all_means = ' '.join([str("{0:.4f}".format(mean)) for mean in means])
        print("{:<12}".format(task) + all_means)

    # Make Boxplot
    plot.figure(figsize=(9,6))
    plot.boxplot([
        load_times('FA', 'total'), 
        load_times('GA', 'total'),
        load_times('B', 'total'),
        load_times('C', 'total'),
        load_times('Start', 'total'),
        load_times('Stub', 'total')
    ])

    plot.title('Feature Computation Time')
    plot.ylabel('Total Time Elapsed (s)')
    plot.xlabel('Quality')
    plot.xticks([1,2,3,4,5,6], ['FA', 'GA', 'B', 'C', 'Start', 'Stub'])
    plot.ylim(0, 10)
    plot.show()


#fetch_computation_times()
analyze_computation_times()
