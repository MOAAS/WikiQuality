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

    # cite
    print(cite_ids(metric_based_paper_ids, inclusion), len(metric_based_paper_ids))
    print(cite_ids(dl_fulltext_paper_ids, inclusion), len(dl_fulltext_paper_ids))
    print(cite_ids(feature_analysis_paper_ids, inclusion), len(feature_analysis_paper_ids))
    print(cite_ids(quality_flaws_paper_ids, inclusion), len(quality_flaws_paper_ids))
    print(cite_ids(regression_paper_ids, inclusion), len(regression_paper_ids))
    print(cite_ids(viz_ids, inclusion), len(viz_ids))
    

cites()