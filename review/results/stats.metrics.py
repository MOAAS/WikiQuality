from csvs.loader import general

def analyze_summary():
    print("========== SUMMARY ==========")
    # papers in general that type includes 'metric'
    metric_papers = [p for p in general if 'metric' in p['Type'].lower()]
    metric_based_papers = [p for p in general if 'metric-based' in p['Type'].lower()]
    metric_based_only_papers = [p for p in general if 'metric-based' == p['Type'].lower()]


    print("Papers that use metrics': ", len(metric_papers))
    print("Papers that use metrics-based': ", len(metric_based_papers))
    print("Papers that use metrics-based only': ", len(metric_based_only_papers))

analyze_summary()