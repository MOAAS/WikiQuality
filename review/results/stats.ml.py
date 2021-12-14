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
papers_using_valid_metrics = [p for p in papers_with_ml if (
    'Accuracy' in p['Perf. Metric'] or 'AUC' in p['Perf. Metric'] or 'F1' in p['Perf. Metric']
)]
papers_not_using_valid_metrics = [p for p in papers_with_ml if (
    'Accuracy' not in p['Perf. Metric'] and 'AUC' not in p['Perf. Metric'] and 'F1' not in p['Perf. Metric']
)]


def analyze_summary():
    print("========== SUMMARY ==========")

    print("Papers without ML: ", len(papers_without_ml))
    print("Papers with ML: ", len(papers_with_ml))
    print("Papers with classical ML: ", len(papers_with_classical))
    print("Papers with DL: ", len(papers_with_dl))
    print("Papers with valid metrics: ", len(papers_using_valid_metrics))
    print("Papers with invalid metrics: ", len(papers_not_using_valid_metrics))

    num_algos = [int(p['# Algorithms']) for p in papers_with_ml if p['# Algorithms'] != '?']
    print("Total # Experiments: ", sum(num_algos))
    print("Average # Experiments: ", sum(num_algos) / len(num_algos))
    print("Median # Experiments: ", sorted(num_algos)[len(num_algos) // 2])


    #print(latex.cite_ids([p['Id'] for p in papers_with_classical], inclusion))
    #print(latex.cite_ids([p['Id'] for p in papers_with_dl], inclusion))

def analyze_dl_cl_years():
    def get_year_of_paper(id):
        for p in inclusion:
            if p['Id'] == id:
                return int(p['Year'])
        return -1

    plt.boxplot([get_year_of_paper(p['Id']) for p in papers_with_classical], positions=[1], widths=0.6, patch_artist=True, boxprops=dict(facecolor='#1f77b4'), medianprops=dict(color='#000000'))
    plt.boxplot([get_year_of_paper(p['Id']) for p in papers_with_dl], positions=[2], widths=0.6, patch_artist=True, boxprops=dict(facecolor='#ff7f0e'), medianprops=dict(color='#000000'))
    plt.xticks([1, 2], ['Classical ML', 'Deep Learning'])
    plt.yticks(np.arange(2005, 2025, 2))
    plt.ylabel('Year')

    # label size
    plotsaver.show_and_save(plt, 'results/charts/dl_years.pdf')

def analyze_class_num():
    # separate papers with dl and cl and both
    num_classes_cl = [str(p['# Classes']) for p in papers_with_classical if p['# Classes'] != '?' and p['# Classes'] != 'N/A']
    num_classes_dl = [str(p['# Classes']) for p in papers_with_dl if p['# Classes'] != '?' and p['# Classes'] != 'N/A']
    num_classes_both = [str(p['# Classes']) for p in papers_with_ml if p['# Classes'] != '?' and p['# Classes'] != 'N/A' and 'CL' in p['ML'] and 'DL' in p['ML']]

    # make stacked bar chart
    ticks = np.arange(2, 8, 1)
    plt.bar(ticks, [num_classes_cl.count(str(i)) for i in range(2, 8, 1)], color='#1f77b4')
    plt.bar(ticks, [num_classes_dl.count(str(i)) for i in range(2, 8, 1)], bottom=[num_classes_cl.count(str(i)) for i in ticks], color='#ff7f0e')
    plt.bar(ticks, [num_classes_both.count(str(i)) for i in range(2, 8, 1)], bottom=[num_classes_cl.count(str(i)) + num_classes_dl.count(str(i)) for i in ticks], color='#2ca02c')
    plt.xticks(ticks,)
    plt.xlabel('# Classes')
    plt.ylabel('# Papers')
    plt.legend(['Classical ML', 'Deep Learning', 'Both'])
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

def analyze_best(type, num_classes):
    papers_with_classes = [p for p in papers_using_valid_metrics if p['# Classes'] == str(num_classes)]
    if type == 'DL': # exclude Trees - it's sometime in CL + DL papers
        papers = [p for p in papers_with_classes if 'DL' in p['ML'] and 'Trees' not in p['Best Algorithm']]
    elif type == 'CL':
        papers = [p for p in papers_with_classes if 'CL' in p['ML']]
    else:
        raise Exception("Unknown type: " + type + ". Must be 'DL' or 'CL'.")

    papers = [{
        'Id': p['Id'],
        'Best Algorithm': p['Best Algorithm'],
        'Performance': float(p['Performance'].split('%')[0]) / 100 if p['Perf. Metric'].startswith('Accuracy') else float(p['Performance'].split('\n')[0]),
        'Perf. Metric': p['Perf. Metric'].split('\n')[0],
        'IR': p['IR'] if (p['IR'] == '?' or p['IR'] == 'N/A') else float(p['IR'].replace(',', '.')),
        'Languages': p['Languages'].split(', '),
    } for p in papers]


    show_only_top = 10
    papers.sort(key=lambda p: float(p['Performance']), reverse=True)
    top_papers = papers[:show_only_top]

    latex.build_template('results/latex/performance.template', 'results/latex/performance.' + str(type) + "." + str(num_classes) + 'class.tex', {
        'NUM_CLASS': num_classes,
        'EXTRA_CAPTION': '(Top ' + str(show_only_top) + ')' if show_only_top < len(papers) else '',
        'TYPE': type,
        'TYPE_LONG': 'Deep Learning' if type == 'DL' else 'Classical Learning',
        'CONTENT': "\n        ".join([(
            latex.cite_author(paper['Id'], inclusion) + " & " +
            paper['Best Algorithm'] + " & " +
            paper['Perf. Metric'].split(' ')[-1] + " & " +
            (
                '{:.2f}'.format(round(paper['Performance'] * 100, 2)) + '\%' if paper['Perf. Metric'] == 'Accuracy' else
                '{:.2f}'.format(round(paper['Performance'], 2)) if paper['Perf. Metric'] == 'F1-score' else
                '{:.2f}'.format(round(paper['Performance'], 2)) if paper['Perf. Metric'] == 'ROC AUC' else
                'should not happen'        
            ) + " & " +
            ('{:.2f}'.format(round(paper['IR'], 2)) if isinstance(paper['IR'], float) else paper['IR']) + " & " +
            (paper['Languages'][0] if len(paper['Languages']) == 1 else 'Multiple') + " \\\\"
        ) for paper in top_papers]),
        'EXTRA_FOOTER': "'?' indicates that we could not collect enough information about class distribution." if any([p['IR'] == '?' for p in top_papers]) else ''
    })

analyze_summary()
#analyze_deep_vs_classical() # REMOVED
#analyze_dl_cl_years() # REMOVED
analyze_class_num()
analyze_best('CL', 6)
analyze_best('CL', 2)
analyze_best('DL', 6)
analyze_best('DL', 2)
