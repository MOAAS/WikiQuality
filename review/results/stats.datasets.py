from csvs.loader import inclusion_but_as_dict as inclusion_dict
from csvs.loader import general

import helpers.plot_saver as plotsaver

import matplotlib.pyplot as plt
import numpy as np
import re

for p in general:
    p['Dataset Size'] = re.sub(r'\s+', '', p['Dataset Size'])
papers_with_dataset = [p for p in general if p['Dataset Size'] != '?' and p['Dataset Size'] != 'N/A']

papers_without_ml = [p for p in papers_with_dataset if p['ML'] == "N/A"]
papers_with_ml = [p for p in papers_with_dataset if p['ML'] != "N/A"]
papers_with_classical = [p for p in papers_with_dataset if 'CL' in p['ML']]
papers_with_dl = [p for p in papers_with_dataset if 'DL' in p['ML']]

def analyze_summary():
    # average dataset size of ML and non-ML papers
    print("========== SUMMARY ==========")

    print("Average dataset size of ML papers: ", np.mean([int(p['Dataset Size']) for p in papers_with_ml]))
    print("Average dataset size of non-ML papers: ", np.mean([int(p['Dataset Size']) for p in papers_without_ml]))
    print("Average dataset size of all papers: ", np.mean([int(p['Dataset Size']) for p in papers_with_dataset]))
    print("Average dataset size of CL papers: ", np.mean([int(p['Dataset Size']) for p in papers_with_classical]))
    print("Average dataset size of DL papers: ", np.mean([int(p['Dataset Size']) for p in papers_with_dl]))

def analyze_topics():
    print("========== TOPICS ==========")
    topics = {}
    with_topic = [p for p in general if p['Topics'] != '?' and p['Topics'] != 'N/A']
    for p in with_topic:
        for t in p['Topics'].split(', '):
            if t not in topics:
                topics[t] = 0
            topics[t] += 1
    topics = {k: v for k, v in topics.items() if v > 1}
    topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    for t in topics:
        print(t[0], t[1])

def analyze_overall_bubble():
    info = [{
        'ML': p['ML'],
        'Year': int(inclusion_dict[p['Id']]['Year']),
        'Size': int(p['Dataset Size']),
        'Langs': len(p['Languages'].split(',')) if p['Languages'] != '?' else 1,        
    } for p in papers_with_dataset]

    # bubble chart: x is year, y is size, size is # langs, color is ML
    plt.scatter(
        [p['Year'] for p in info], 
        [p['Size'] for p in info], 
        s=[p['Langs'] * 20 for p in info], 
        c=['#1f77b4' if p['ML'] == 'N/A' else '#ff7f0e' for p in info],
        alpha=0.75
    )
    plt.xlabel('Publication Year')
    plt.ylabel('Dataset Size (# Publications)')
    plt.yscale('log')

    # legend is only shown for the first plot
    plt.scatter([], [], c='#1f77b4', label='Non-ML')
    plt.scatter([], [], c='#ff7f0e', label='ML')
    plt.legend()
    
    plt.xticks(np.arange(2005, 2025, 2))
    plt.ylim(10, 10**8)

    plotsaver.show_and_save(plt, 'results/charts/datasets.pdf')
    

analyze_overall_bubble()

analyze_summary()
analyze_topics()