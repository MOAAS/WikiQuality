from csvs.loader import inclusion_but_with_more as inclusion
from csvs.loader import general
from csvs.loader import parse_paper_type
import helpers.latex_templating as latex
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

def size_boxplot():
    info = [{
        'Type': {
            'DL': 'Deep Learning',
            'CL': 'Classical Learning',
            'MB': 'Metric-Based',
            'FMC': 'Other',
            'Other': 'Other',
        }[parse_paper_type(p)],
        'Size': int(p['Dataset Size']),
    } for p in papers_with_dataset]

    # box plot (4)
    plt.boxplot([d['Size'] for d in info if d['Type'] == 'Deep Learning'], positions=[1], widths=0.6, showfliers=True, patch_artist=True, boxprops=dict(facecolor='#1f77b4'))
    plt.boxplot([d['Size'] for d in info if d['Type'] == 'Classical Learning'], positions=[2], widths=0.6, showfliers=True, patch_artist=True, boxprops=dict(facecolor='#ff7f0e'))
    plt.boxplot([d['Size'] for d in info if d['Type'] == 'Metric-Based'], positions=[3], widths=0.6, showfliers=True, patch_artist=True, boxprops=dict(facecolor='#2ca02c'))
    plt.boxplot([d['Size'] for d in info if d['Type'] == 'Other'], positions=[4], widths=0.6, showfliers=True, patch_artist=True, boxprops=dict(facecolor='#d62728'))

    plt.xticks([1, 2, 3, 4], ['Deep Learning', 'Classical Learning', 'Metric-Based', 'Other'])
    plt.yscale('log')
    plt.yticks([10, 100, 1000, 10000, 100000, 1000000, 10000000], ['10', '100', '1k', '10k', '100k', '1M', '10M'])
    plt.ylabel('Dataset Size (\# Wikipedia Articles)')

    plotsaver.show_and_save(plt, 'results/charts/datasets.pdf', type="boxplot")
    
def analyze_output():
    print("========== OUTPUT ==========")
    # papers where Output contains dataset.
    papers_with_dataset = [p for p in general if 'Dataset' in p['Output']]
    papers_with_implementation = [p for p in general if 'Implementation' in p['Output']]

    print("Papers with dataset: ", len(papers_with_dataset))
    print("Papers with implementation: ", len(papers_with_implementation))
    print(latex.cite_ids([p['Id'] for p in papers_with_dataset], inclusion))
    print(latex.cite_ids([p['Id'] for p in papers_with_implementation], inclusion))

size_boxplot()

analyze_summary()
analyze_topics()

analyze_output()