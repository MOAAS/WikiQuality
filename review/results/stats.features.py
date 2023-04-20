from csvs.loader import features
from csvs.loader import general

import matplotlib.pyplot as plt
import helpers.latex_templating as latex
import helpers.plot_saver as plotsaver

def make_bar_chart():
    categories = {}
    for feature in features:
        if feature['Category'] not in categories:
            categories[feature['Category']] = {
                'Actionable-Yes': 0,
                'Actionable-No': 0,
                'Multilingual-All': 0,
                'Multilingual-Most': 0,
                'Multilingual-Some': 0,
                'Total': 0
            }
        categories[feature['Category']]['Total'] += 1
        if feature['Actionable'] == 'Yes':
            categories[feature['Category']]['Actionable-Yes'] += 1
        else:
            categories[feature['Category']]['Actionable-No'] += 1
        if feature['Multilingual'] == 'All':
            categories[feature['Category']]['Multilingual-All'] += 1
        elif feature['Multilingual'] == 'Most':
            categories[feature['Category']]['Multilingual-Most'] += 1
        elif feature['Multilingual'] == 'Some':
            categories[feature['Category']]['Multilingual-Some'] += 1

    # sort categories by total number of features
    categories = {k: v for k, v in sorted(categories.items(), key=lambda item: item[1]['Total'], reverse=True)}

    # make bar chart: every category has 3 bars: actionable, multilingual, total
    x = [i for i in range(len(categories))]
    width = 0.2    

    actionable = [categories[c]['Actionable-Yes'] for c in categories]
    non_actionable = [categories[c]['Actionable-No'] for c in categories]
    multilingual_all = [categories[c]['Multilingual-All'] for c in categories]
    multilingual_most = [categories[c]['Multilingual-Most'] for c in categories]
    multilingual_some = [categories[c]['Multilingual-Some'] for c in categories]

    plt.bar([i - width / 2 for i in x], actionable, width=width, label='Actionable')
    plt.bar([i - width / 2 for i in x], non_actionable, width=width, label='Non-actionable', bottom=actionable)

    plt.bar([i + width / 2 for i in x], multilingual_all, width=width, label='Multilingual: All')
    plt.bar([i + width / 2 for i in x], multilingual_most, width=width, label='Multilingual: Most', bottom=multilingual_all)
    plt.bar([i + width / 2 for i in x], multilingual_some, width=width, label='Multilingual: Some', bottom=[multilingual_all[i] + multilingual_most[i] for i in range(len(multilingual_all))])

    #plt.bar(x, [categories[c]['Total'] for c in categories], width=width, label='Total')

    plt.xticks(x, [c for c in categories])
    plt.ylim(0, 125)
    plt.legend()

    # text on top of bars. just one text per category, saying the total number of features
    for i in range(len(x)):
        total = categories[list(categories.keys())[i]]['Total']
        plt.text(x[i], total, str(total), ha='center', va='bottom')

    plt.title("Number of features per category")
    plt.xlabel("Category")
    plt.ylabel("Number of features")


    plotsaver.show_and_save(plt, "results/charts/categories.pdf", size=(8, 4))
    plt.show()

print("Number of features: ", len(features))

def analyze_top_features(category):
    category_features = [f for f in features if f['Category'] == category]
    print("Number of " + category + " features: ", len(category_features))

    use_features = sorted(category_features, key=lambda f: len(f['Papers'].split(', ')), reverse=True) # sort by number of papers
    use_features = use_features[:max(15, int(len(use_features) * 0.25))] # get top 25%, but minimum 15

    latex.build_template('results/latex/features.template', 'results/latex/features.' + category.lower() + '.tex', {
        'USED': 
            'all' if len(use_features) == len(category_features)
            else '15 most used' if len(use_features) == 15 
            else '25\% most used',
        'CATEGORY': category,
        'CONTENT': "\n        ".join([(
            feature['Feature Name'].replace('#', '\\#') + ' & ' + 
            feature['Actionable'] + ' & ' +
            feature['Multilingual'] + ' & ' +
            str(len(feature['Papers'].split(', '))) + ' \\\\'
            # cite_ids(feature['Papers'].split(', '), inclusion) + ' \\\\' # 
        ) for feature in use_features])
    })

def analyze_summary():
    print("========== SUMMARY ==========")
    # top 10 papers by number of features.
    top_papers = sorted(general, key=lambda p: int(p['# Features'].split(' / ')[0]), reverse=True)
    top_papers = top_papers[:20]
    print("Top 10 papers by number of features:")
    print("Id Title # Features")
    for p in top_papers:
        print(p['Id'], p['Title'], p['# Features'])


    # sum of all features
    sum_features = 0
    for p in general:
        sum_features += int(p['# Features'].split(' / ')[0])
    print("Total number of features: ", len(features))
    print("Total number of collected (non-distinct) features: ", sum_features)
    print("Total number of papers that we collected features: ", len( [p for p in general if int(p['# Features'].split(' / ')[0]) > 0]))
    print("Total number of papers that used features: ", len( [p for p in general if int(p['# Features'].split(' / ')[1]) > 0]))


make_bar_chart()

analyze_top_features('Content')
analyze_top_features('Style')
analyze_top_features('Readability')
analyze_top_features('History')
analyze_top_features('Network')
analyze_top_features('Popularity')


analyze_summary()