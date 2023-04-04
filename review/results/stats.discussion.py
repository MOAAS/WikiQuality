from csvs.loader import general
from csvs.loader import inclusion_but_with_more as inclusion

from helpers.latex_templating import cite_ids



def cites():
    print("============= cites =============")
    
    # get all papers where general['type'] = metric-based
    metric_based_paper_ids = [p['Id'] for p in general if 'metric-based' == p['Type'].lower()]
    dl_fulltext_paper_ids = [p['Id'] for p in general if 'DL' in p['Type'] and 'full-text' in p['Type'].lower()]
    feature_analysis_paper_ids = [p['Id'] for p in general if 'feature importance analysis' in p['Notes'].lower()]
    quality_flaws_paper_ids = [p['Id'] for p in general if 'QFs' in p['Type']]
    regression_paper_ids = [p['Id'] for p in general if 'MSE' in p['Perf. Metric']]
    viz_ids = [p['Id'] for p in general if 'viz' in p['Type'].lower()]
    implementation_ids = [p['Id'] for p in general if 'implementation' in p['Output'].lower()]

    # cite
    print(cite_ids(metric_based_paper_ids, inclusion), len(metric_based_paper_ids))
    print(cite_ids(dl_fulltext_paper_ids, inclusion), len(dl_fulltext_paper_ids))
    print(cite_ids(feature_analysis_paper_ids, inclusion), len(feature_analysis_paper_ids))
    print(cite_ids(quality_flaws_paper_ids, inclusion), len(quality_flaws_paper_ids))
    print(cite_ids(regression_paper_ids, inclusion), len(regression_paper_ids))
    print(cite_ids(viz_ids, inclusion), len(viz_ids))
    print(cite_ids(implementation_ids, inclusion), len(implementation_ids))


def matrix():
    criteria = [
        { 'name': 'DL', 'condition': lambda p: 'DL' in p['Type'] },
        { 'name': 'CL', 'condition': lambda p: 'classical' in p['Type'] },
        { 'name': 'classification', 'condition': lambda p: 'MSE' not in p['Perf. Metric'] and p['ML'] != 'N/A' },
        { 'name': 'regression', 'condition': lambda p: 'MSE' in p['Perf. Metric'] },
        { 'name': 'Balanced', 'condition': lambda p: p['IR'] != 'N/A' and p['IR'] != '?' and float(p['IR'].replace(',','.')) < 1.05 },
        { 'name': 'uses features', 'condition': lambda p: p['# Features'] != '0/0' },
        { 'name': 'uses metrics', 'condition': lambda p: p['Metrics'] != 'Yes' }, 
        { 'name': 'Feature Analysis', 'condition': lambda p: 'feature importance analysis' in p['Notes'].lower() },
        { 'name': 'QFs', 'condition': lambda p: 'QFs' in p['Type'] },
        { 'name': 'M.L.', 'condition': lambda p: len(p['Languages'].split(', ')) > 1 },
        { 'name': 'Actionable', 'condition': lambda p: 'actionable' in p['Title'].lower() },
        { 'name': 'viz', 'condition': lambda p: 'viz' in p['Type'].lower() },
    ]

    # make a square matrix
    matrix = [[0 for _ in range(len(criteria))] for _ in range(len(criteria))]
    for i, c1 in enumerate(criteria):
        for j, c2 in enumerate(criteria):
            matrix[i][j] = len([p for p in general if c1['condition'](p) and c2['condition'](p)])

    # print matrix
    # is a diagonal matrix, so only print upper triangle
    print('   ', end='')
    print(' & '.join([c['name'][:3].rjust(3) for c in criteria]))
    for i, row in enumerate(matrix):
        print(criteria[i]['name'][:3].rjust(3), end='')
        if i == 0:
            print(' & '.join([str(c).rjust(3) for c in row]))
        else:
            print(' & '.join([' - ' for _ in range(i)]) + " & ", end='')
            print(' & '.join([str(c).rjust(3) for c in row[i:]]))

    #


    print()
    for row in matrix:
        print(' & '.join([str(c).rjust(3) for c in row]))



cites()
#matrix()