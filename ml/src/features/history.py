from statistics import stdev

# Unimplemented features:
# - HD: Need to fetch talk page first, probably do it when fetching the pages
# - HPROB: Very complex, will probably not compute it
# - HQAC: A bit computationally expensive
# - HABPR, HEBPR, HTC, HPC: Very specific metrics from literature review, hard to compute
# - HERV/HERNV: Would be easy to add if needed (check if is revert and says vandalism), but idk what they mean by recently

# Adapted features
# - HRML: Do not have access to revision content (very computationally expensive, so used the revision size instead)

HISTORY_FEATURES = [
    'HA', 'HAPR', 'HRPD', 'HRPC', 'HRPCSD', 'HR', 'HC',  'HRC', 'HAC', 'HRCPC', 'HACPC', 'HRCPAC', 'HREV', 
    'HREVPR', 'HRML', 'HREC', 'HRECPR', 'HACT', 'HACTPR', 'HOCCPR', 'HSSLE'
]

def compute_history_features(revisions):

    ft = {}

    # Deleted revisions may have their comments and users removed, so we check for that first
    for revision in revisions:
        if 'comment' not in revision:
            revision['comment'] = ''

    recent_revs = [revision for revision in revisions if revision['age'] < 180] # last 3 months
    contributors = set([revision['user'] for revision in revisions if 'user' in revision])
    contributor_revs = { contributor: 0 for contributor in contributors }
    for revision in revisions:
        if 'user' in revision:
            contributor_revs[revision['user']] += 1

    sorted_users = sorted(contributor_revs.items(), key=lambda x: x[1], reverse=True)

    active_contributors = set([user[0] for user in sorted_users[:int(len(sorted_users) * 0.05)]]) # get top 5% of the list
    occasional_contributors = set([contributor for contributor, revs in sorted_users if revs < 4]) # less than 4 revisions
    
    ft['HA'] = revisions[-1]['age'] + 1 # Age (days)
    ft['HAPR'] = ft['HA'] / len(revisions) # Age per review
    ft['HRPD'] = len(revisions) / ft['HA'] # Reviews per day
    ft['HRPC'] = len(revisions) / len(contributors) # Reviews per contributor
    ft['HRPCSD'] = stdev(contributor_revs.values()) if len(contributors) > 1 else 0 # Reviews per contributor standard deviation

    ft['HR'] = len(revisions) # Review count
    ft['HC'] = len(contributors) # Contributor count    
    ft['HRC'] = len([contributor for contributor in contributors if not contributor[0].isdigit()]) # Registered contributor count (start with digit -> IP -> anonymous)
    ft['HAC'] = ft['HC'] - ft['HRC'] # Anonymous contributor count
    ft['HRCPC'] = ft['HRC'] / ft['HC'] # Registered contributor count per contributor
    ft['HACPC'] = ft['HAC'] / ft['HC'] # Anonymous contributor count per contributor
    ft['HRCPAC'] = ft['HRC'] / ft['HAC'] if ft['HAC'] > 0 else 0 # Registered contributor per anonymous contributor

    ft['HREV'] = len([revision for revision in revisions if revision['comment'].lower().startswith("rev")]) # Revert count
    ft['HREVPR'] = ft['HREV'] / len(revisions) # Revert count per review
    
    ft['HRML'] = recent_revs[0]['size'] - recent_revs[-1]['size'] if len(recent_revs) > 1 else 0 # Modified lines rate (adapted)

    ft['HREC'] = len(recent_revs) # Recent review count
    ft['HRECPR'] = ft['HREC'] / len(revisions) # Recent review count per review

    for revision in revisions:
        if 'user' not in revision:
            revision['user'] = ''

    ft['HACT'] = len([revision for revision in revisions if revision['user'] in active_contributors]) # Active review count
    ft['HACTPR'] = ft['HACT'] / len(revisions) # Active review count per review
    ft['HOCCPR'] = len([revision for revision in revisions if revision['user'] in occasional_contributors]) / len(revisions) # Occasional review count per review

    ft['HSSLE'] = revisions[0]['age'] * 24 * 60 * 60 # Seconds since last edit
    return ft
