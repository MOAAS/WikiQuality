import csv

from csvs.loader import eligibility
from csvs.loader import inclusion
from csvs.loader import general
from csvs.loader import features

from csvs.loader import titles
from csvs.loader import abstracts
from csvs.loader import fulltexts



def identification_stats():
    print("============= IDENTIFICATION STATS =============")
    for database in set([x['Database'] for x in titles]):
        print(database, ': ', len([x for x in titles if x['Database'] == database]))
    print('All Titles: ', len(titles))
    duplicates = [x for x in titles if 'Duplicate' in x['Include']]
    print('Duplicates: ', len(duplicates))
    print('Non-duplicates: ', len(titles) - len(duplicates))

def screening_stats():
    print("============= SCREENING STATS =============")
    print('All Titles: ', len(titles))

    print('Duplicates: ', len([x for x in titles if 'Duplicate' in x['Include']]))
    print('Nos: ', len([x for x in titles if x['Include'] == 'No']))
    print('All Abstracts: ', len(abstracts))

    print(
        'Nos: ', len([x for x in abstracts if x['Include'] == 'No']), 
        '(of which no access: ', len([x for x in abstracts if x['Notes'].find('No access') != -1]), ')'
    )
          
    print('All Full texts (w/o citation track): ', len([x for x in fulltexts if int(x['Id']) < 1000]))

def eligibility_stats():
    print("============= ELIGIBILITY STATS =============")
    initial = [x for x in eligibility if int(x['Id']) < 1000]
    tracked = [x for x in eligibility if int(x['Id']) >= 1000]
    print('Initial: ', len(initial))
    print('Excluded (initial): ', len( [x for x in initial if x['Include'] == 'No']))
    print('Included (initial): ', len( [x for x in initial if x['Include'] == 'Yes']))
    
    print('Tracked: ', len(tracked))
    print('Excluded (tracked): ', len( [x for x in tracked if x['Include'] == 'No']))
    print('Included (tracked): ', len( [x for x in tracked if x['Include'] == 'Yes']))

    print('Total: ', len(initial) + len(tracked))

def inclusion_stats():
    print("============= INCLUSION STATS =============")
    print('All Included', len(inclusion))
    print('Average Q1: ', sum([int(x['Q1 [0, 3]']) for x in inclusion]) / len(inclusion))
    print('Average Q2: ', sum([int(x['Q2 [0, 3]']) for x in inclusion]) / len(inclusion))
    print('Average Q3: ', sum([int(x['Q3 [0, 3]']) for x in inclusion]) / len(inclusion))
    print('Average Q4: ', sum([int(x['Q4 [0, 1]']) for x in inclusion]) / len(inclusion))
    print('Average Total: ', sum([int(x['Total [0, 10]']) for x in inclusion]) / len(inclusion))

    print('Avg. Refs.: ', sum([int(x['Refs.']) for x in inclusion]) / len(inclusion))
    print('Avg. Cits.: ', sum([int(x['Cits.']) for x in inclusion]) / len(inclusion))

def tracking_stats():
    print("============= TRACKING STATS =============")


    print('Backward Tracked: ', len([x for x in inclusion if x['Backward Tracked'] == 'Yes']))
    print('Forward Tracked: ', len([x for x in inclusion if x['Forward Tracked'] == 'Yes']))
    print('Results from Tracking: ', len([x for x in inclusion if int(x['Id']) >= 1000]))
    
    refs_followed = sum([int(x['Refs.']) for x in inclusion if x['Backward Tracked'] == 'Yes' or x['Forward Tracked'] == 'Yes'])
    cits_followed = sum([int(x['Cits.']) for x in inclusion if x['Backward Tracked'] == 'Yes' or x['Forward Tracked'] == 'Yes'])
    obtained_from_tracking = len([x for x in eligibility if int(x['Id']) >= 1000])
    print('Total Refs. Followed: ', refs_followed)
    print('Total Cits. Followed: ', cits_followed)
    print('Total Refs. + Cits. Followed: ', refs_followed + cits_followed)
    print('Ignored: ', refs_followed + cits_followed - obtained_from_tracking)

identification_stats()
screening_stats()
eligibility_stats()
inclusion_stats()
tracking_stats()