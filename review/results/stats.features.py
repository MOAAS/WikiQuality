from csvs.loader import features
from csvs.loader import general

import matplotlib.pyplot as plt
import helpers.latex_templating as latex

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
    print("Number of " + category + " features: ", len(use_features))

    use_features = sorted(use_features, key=lambda f: len(f['Papers']), reverse=True) # sort by number of papers
    use_features = use_features[:max(15, int(len(use_features) * 0.25))] # get top 25%, but minimum 15

    latex.build_template('results/latex/features.template', 'results/latex/features.' + category.lower() + '.tex', {
        'CATEGORY': category,
        'CONTENT': "\n        ".join([(
            feature['Feature Name'].replace('#', '\\#') + ' & ' + 
            ('Yes' if feature['Actionable'] == 'Yes' else 'No') + ' & ' + 
            ('Yes' if feature['Multilingual'] == 'Yes' else 'No') + ' & ' +
            str(len(feature['Papers'])) + ' \\\\'
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
# make_pie_chart()

analyze_top_features('Content')
analyze_top_features('Style')
analyze_top_features('Readability')
analyze_top_features('History')
analyze_top_features('Network')
analyze_top_features('Popularity')


analyze_summary()