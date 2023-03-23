from csvs.loader import features
from csvs.loader import inclusion

import matplotlib.pyplot as plt

from latex.templating import build_template 

def make_pie_chart():
    categories = {}
    for feature in features:
        if feature['Category'] not in categories:
            categories[feature['Category']] = 0
        categories[feature['Category']] += 1
    print("Categories: ", categories)

    labels = list(categories.keys())
    labels = [l + ' (' + str(categories[l]) + ')' for l in labels]
    sizes = list(categories.values())
    plt.pie(
        sizes, labels=labels, # 6 colors
        colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#ff99ff', '#ffff99'],
        autopct=(lambda pct: '' if pct < 2 else '{:.1f}%'.format(pct)), 
        startangle=135
    )
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig("results/charts/categories.pdf", dpi=100, bbox_inches='tight', pad_inches=0.1)
    plt.show()

print("Number of features: ", len(features))

def analyze_top_features(category):
    use_features = [f for f in features if f['Category'] == category]
    print("Number of features: ", len(use_features))

    use_features = sorted(use_features, key=lambda f: len(f['Papers']), reverse=True) # sort by number of papers
    use_features = use_features[:max(15, int(len(use_features) * 0.25))] # get top 25%, but minimum 15

    # print name, number of papers, actionable (X or -), multilingual
    build_template('results/latex/features.template', 'results/latex/features.' + category.lower() + '.tex', {
        'CATEGORY': category,
        'CONTENT': 'test'
    })
    # read features.template to string
    # for feature in use_features:
    #    print(feature['Feature Name'], '&', len(feature['Papers']), '&', 'X' if feature['Actionable'] else '-', '&', 'X' if feature['Multilingual'] else '-', '')


# make_pie_chart()

analyze_top_features('Content')
analyze_top_features('Style')
analyze_top_features('Readability')
analyze_top_features('History')
analyze_top_features('Network')
analyze_top_features('Popularity')