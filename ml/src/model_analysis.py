import time
import matplotlib.pyplot as plot
import pickle
import os
import random
import wikiapi

from features.main import compute_features

model_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
titles_folder = os.path.join(os.path.dirname(__file__), '..', 'titles')
report_times_folder = os.path.join(os.path.dirname(__file__), '..', 'reports', 'times')

def load_model(modelname):
    with open(f'{model_folder}/{modelname}/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(f'{model_folder}/{modelname}/features.pkl', 'rb') as f:
        features = pickle.load(f)

    return model, features


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

def analyze_feature_importance(modelname):
    model, features = load_model(modelname)
    importance = model.feature_importances_

    # make dictonary of feature names and importance values
    feature_importance = dict(zip(features, importance))

    # get the top 20 and bottom 20 features
    top_20_1 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[0:10])
    top_20_2 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[11:20])
    bottom_20_1 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)[0:10])
    bottom_20_2 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)[11:20])
    
    figure_top, axis_top = plot.subplots(2, 1,figsize=(9,6))
    figure_bot, axis_bot = plot.subplots(2, 1,figsize=(9,6))

    axis_top[0].set_title('Feature Importance: Top 20')
    axis_top[0].bar(top_20_1.keys(), top_20_1.values())
    axis_top[1].bar(top_20_2.keys(), top_20_2.values())

    #figure.tight_layout()

    axis_bot[0].set_title('Feature Importance: Bottom 20')
    axis_bot[0].bar(bottom_20_1.keys(), bottom_20_1.values())
    axis_bot[1].bar(bottom_20_2.keys(), bottom_20_2.values())

    plot.draw()
    plot.pause(1) # https://stackoverflow.com/a/22899859
    plot.waitforbuttonpress(0)
    plot.close(figure_bot)
    plot.close(figure_top)

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
            print(title)
            start = time.time()
            wikitext = wikiapi.getWikiText(title)
            if wikitext == '':
                continue           

            wikitext_elapsed = time.time() - start
            
            feats = compute_features(title, wikitext, 0)
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

analyze_computation_times()

# interquartil stuff for analysis
    


#analyze_feature_importance("CSRH6/forest_r")
#fetch_computation_times()
