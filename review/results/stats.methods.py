from csvs.loader import general
from csvs.loader import inclusion_but_with_more as inclusion

import helpers.plot_saver as plotsaver
import helpers.latex_templating as latex

import matplotlib.pyplot as plt


def method_stats():
    print("============= METHOD STATS =============")
    print('Number of papers: ' + str(len(inclusion)))

    paper_ids_with_ml = set([paper['Id'] for paper in general if paper['ML'] != 'N/A'])
    paper_ids_with_metric_based = set([paper['Id'] for paper in general if 'metric-based' in paper['Type']])
    paper_ids_with_featscorrelates = set([paper['Id'] for paper in general if 'features + correlates' in paper['Type']])

    paper_ids_with_classical_features = set([paper['Id'] for paper in general if 'classical + features' in paper['Type']])
    paper_ids_with_dl = set([paper['Id'] for paper in general if 'DL' in paper['ML']])

    print('Number of papers with ML: ' + str(len(paper_ids_with_ml)))
    print('Number of papers with metric-based: ' + str(len(paper_ids_with_metric_based)))
    print('Number of papers with features + correlates: ' + str(len(paper_ids_with_featscorrelates)))
    print('Number of papers with classical + features: ' + str(len(paper_ids_with_classical_features)))
    print('Number of papers with DL: ' + str(len(paper_ids_with_dl)))

    print('Number of papers with ML or metric-based: ' + str(len(paper_ids_with_ml | paper_ids_with_metric_based)))
    print('Number of papers with ML or features + correlates: ' + str(len(paper_ids_with_ml | paper_ids_with_featscorrelates)))
    print('Number of papers with metric-based or features + correlates: ' + str(len(paper_ids_with_metric_based | paper_ids_with_featscorrelates)))
    print('Big three methods: ' + str(len(paper_ids_with_metric_based | paper_ids_with_classical_features | paper_ids_with_dl)))
    print('Big four methods: ' + str(len(paper_ids_with_metric_based | paper_ids_with_classical_features | paper_ids_with_dl | paper_ids_with_featscorrelates)))

    latex.build_template('results/latex/methods.template', 'results/latex/methods.tex', {
        'METRIC_BASED': len(paper_ids_with_metric_based),
        'METRIC_BASED_CITE': latex.cite_ids(paper_ids_with_metric_based, inclusion),
        'CL_FEATURES': len(paper_ids_with_classical_features),
        'CL_FEATURES_CITE': latex.cite_ids(paper_ids_with_classical_features, inclusion),
        'DL': len(paper_ids_with_dl),
        'DL_CITE': latex.cite_ids(paper_ids_with_dl, inclusion),
        'CORRELATES': len(paper_ids_with_featscorrelates),
        'CORRELATES_CITE': latex.cite_ids(paper_ids_with_featscorrelates, inclusion),
    })

def languages_stats():
    print("========== LANGUAGES ==========")
    no_english = [paper for paper in general if 'English' not in paper['Languages'] and '?' not in paper['Languages'] and 'N/A']
    
    langs = {}
    with_langs = [p for p in general if p['Languages'] != '?' and p['Languages'] != 'N/A']
    for p in with_langs:
        for l in p['Languages'].split(', '):
            if l not in langs:
                langs[l] = {
                    'Non-ML': 0,
                    'ML': 0,
                    'Total': 0,
                }
            langs[l]['Total'] += 1
            if p['ML'] == 'N/A':
                langs[l]['Non-ML'] += 1
            else:
                langs[l]['ML'] += 1
    langs = {k: v for k, v in langs.items() if v['Total'] > 5}
    langs = sorted(langs.items(), key=lambda x: x[1]['Total'], reverse=True)

    names = [l[0] for l in langs]
    counts = [l[1]['Total'] for l in langs]
    counts_noml = [l[1]['Non-ML'] for l in langs]
    counts_ml = [l[1]['ML'] for l in langs]
    
    # stacked bar chart
    plt.bar(names, counts_noml, label='Non-ML')
    plt.bar(names, counts_ml, label='ML', bottom=counts_noml)

    plt.xticks(rotation=45)
    plt.xlabel('Wikipedia Version')
    plt.ylabel('Number of Publications')
    plt.legend()

    # add labels to bars
    for i, v in enumerate(counts):
        plt.text(i, v + 0.5, str(v), ha='center')

    print('Number of papers not assesing English: ' + str(len(no_english)))
    print('Number of papers with languages: ' + str(langs))
    plotsaver.show_and_save(plt, 'results/charts/languages.pdf', size=(8, 4))

    # count languages per paper
    counts = {}
    for p in with_langs:
        num_langs = len(p['Languages'].split(', '))
        if num_langs not in counts:
            counts[num_langs] = {
                'Non-ML': 0,
                'ML': 0,
            }
        if p['ML'] == 'N/A':
            counts[num_langs]['Non-ML'] += 1
        else:
            counts[num_langs]['ML'] += 1
    # sort by count
    counts = sorted(counts.items(), key=lambda x: x[0])
    counts_overone = [(c[0], c[1]) for c in counts if c[0] > 1]


    def draw_plot(plt, counts):
        # stacked bar chart
        names = [c[0] for c in counts]
        ml_counts = [c[1]['ML'] for c in counts]
        non_ml_counts = [c[1]['Non-ML'] for c in counts]

        plt.bar(names, non_ml_counts, label='Non-ML')
        plt.bar(names, ml_counts, bottom=non_ml_counts, label='ML')

    fig, main_axis = plt.subplots(figsize=(8, 4))
    draw_plot(main_axis, counts)
    main_axis.set_xlabel('Number of asssessed Wikipedia Versions')
    main_axis.set_ylabel('Number of Publications')

    # add grid to main plot, and move grid to back
    main_axis.grid(True, axis='both', which='both', color='0.8', linestyle=':', linewidth=1, zorder=1)
    main_axis.set_axisbelow(True)
    for spine in main_axis.spines.values():
        spine.set_zorder(2)
    
    small_axis = fig.add_axes([0.3, 0.4, 0.58, 0.45])
    draw_plot(small_axis, counts_overone)
    small_axis.set_xticks([c[0] for c in counts_overone])
    small_axis.set_xlim(1, 60)
    small_axis.tick_params(axis='both', which='major', labelsize=8)
    small_axis.set_yticks([0, 1, 2, 3])
    small_axis.legend()

    # add arrow between plots
    main_axis.annotate('', xytext=(6, 22), xy=(11, 42),  arrowprops=dict(facecolor='black', arrowstyle='<->'))

    plotsaver.show_and_save(plt, 'results/charts/languages_count.pdf', size=(8, 4))
    print('Number of papers with one language: (non-ml/ml)', str(counts[0][1]['Non-ML']), counts[0][1]['ML'])
    print('Number of papers per num languages: ', counts)

method_stats()
languages_stats()