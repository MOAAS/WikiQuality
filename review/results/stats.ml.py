from csvs.loader import inclusion_but_with_more as inclusion
from csvs.loader import general

import helpers.latex_templating as latex

import matplotlib.pyplot as plt
import numpy as np
import helpers.plot_saver as plotsaver

papers_without_ml = [p for p in general if p['ML'] == "N/A"]
papers_with_ml = [p for p in general if p['ML'] != "N/A"]
papers_with_classical = [p for p in general if 'CL' in p['ML']]
papers_with_dl = [p for p in general if 'DL' in p['ML']]


def analyze_summary():
    print("========== SUMMARY ==========")

    print("Papers without ML: ", len(papers_without_ml))
    print("Papers with ML: ", len(papers_with_ml))
    print("Papers with classical ML: ", len(papers_with_classical))
    print("Papers with DL: ", len(papers_with_dl))

    num_algos = [int(p['# Algorithms']) for p in papers_with_ml if p['# Algorithms'] != '?']
    print("Total # Experiments: ", sum(num_algos))
    print("Average # Experiments: ", sum(num_algos) / len(num_algos))
    print("Median # Experiments: ", sorted(num_algos)[len(num_algos) // 2])

def analyze_dl_cl_years():
    def get_year_of_paper(id):
        for p in inclusion:
            if p['Id'] == id:
                return int(p['Year'])
        return -1

    plt.boxplot([get_year_of_paper(p['Id']) for p in papers_with_classical], positions=[1], widths=0.6, patch_artist=True, boxprops=dict(facecolor='#1f77b4'))
    plt.boxplot([get_year_of_paper(p['Id']) for p in papers_with_dl], positions=[2], widths=0.6, patch_artist=True, boxprops=dict(facecolor='#ff7f0e'))
    plt.xticks([1, 2], ['Classical ML', 'Deep Learning'])
    plt.yticks(np.arange(2005, 2025, 2))
    plt.ylabel('Year')

    # median lines must be black
    for line in plt.gca().get_lines():
        line.set_color('black')

    # label size
    plotsaver.show_and_save(plt, 'results/charts/dl_years.pdf')

def analyze_class_num():
    num_classes = [str(p['# Classes']) for p in papers_with_ml if p['# Classes'] != '?' and p['# Classes'] != 'N/A']

    # make bar chart
    plt.bar(np.arange(2, 8, 1), [num_classes.count(str(i)) for i in range(2, 8, 1)], color='#1f77b4')
    plt.xticks(np.arange(2, 8, 1), np.arange(2, 8, 1))
    plt.xlabel('# Classes')
    plt.ylabel('# Papers')
    plotsaver.show_and_save(plt, 'results/charts/num_classes.pdf')

def analyze_deep_vs_classical():
    # make venn diagram
    from matplotlib_venn import venn2

    papers_both = [p for p in papers_with_ml if 'CL' in p['ML'] and 'DL' in p['ML']]

    venn2(
        subsets = (len(papers_with_classical), len(papers_with_dl), len(papers_both)), 
        set_labels = ('Classical ML', 'Deep Learning'),
        set_colors = ('#1f77b4', '#ff7f0e'),
        alpha = 0.7,
    )

    # label size
    for text in plt.gca().texts:
        text.set_fontsize(14)

    plotsaver.show_and_save(plt, 'results/charts/dl_venn.pdf', (6, 4))


def analyze_best(num_classes):
    papers = [p for p in papers_with_ml if p['# Classes'] == str(num_classes) and 'Accuracy' in p['Perf. Metric']]
    papers.sort(key=lambda p: float(p['Performance'].split('%')[0]), reverse=True)
    papers = papers[:10]
    
    #for p in papers:
    #    print(p['Id'], p['ML'], p['# Algorithms'], p['Best Algorithm'], p['Performance'].replace('\n', ' '), p['Perf. Metric'].replace('\n', ' '))    

    latex.build_template('results/latex/performance.template', 'results/latex/performance.' + str(num_classes) + 'class.tex', {
        'NUM_CLASS': num_classes,
        'CONTENT': "\n        ".join([(
            latex.cite_author(paper['Id'], inclusion) + " & " +
            paper['Best Algorithm'] + " & " +
            paper['Performance'].split('\n')[0].replace("%", "\%") + " & " +
            paper['IR'] + " \\\\"
        ) for paper in papers])
    })

analyze_summary()
analyze_deep_vs_classical()
analyze_dl_cl_years()
analyze_class_num()
analyze_best(6)
analyze_best(2)
