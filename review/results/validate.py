import re
from csvs.loader import eligibility
from csvs.loader import inclusion
from csvs.loader import general
from csvs.loader import features

general_dict = {g['Id']: g for g in general}
features_dict = {}
for f in features:
    ids = [i.strip() for i in f['Papers'].split(',')]
    for id in ids:
        if id not in features_dict:
            features_dict[id] = []
        features_dict[id].append(f['Feature Name'])

    
def validate_column_values(csv, column, values):
    for i, row in enumerate(csv):
        if row[column] not in values:
            print('Invalid value "{}" in column "{}" in row {} (ID={}).'.format(row[column], column, i, row['Id']))
            return False
        
def validate_column_number(csv, column, allow_undefined=False):
    for i, row in enumerate(csv):
        if row[column] == '?' and allow_undefined:
            continue
        try:
            int(row[column])
        except ValueError:
            print('Invalid number "{}" in column "{}" in row {} (ID={}).'.format(row[column], column, i, row['Id']))
            return False
    return True

def print_row_error(file, row, reason):
    print('Invalid row (ID={}) in {}. {}'.format(row, file, reason))
    return False

def validate_eligibility():
    print('Validating eligibility.csv...')
    validate_column_number(eligibility, 'Id')
    validate_column_values(eligibility, 'Features/Metrics', ['Yes', 'No', ''])
    validate_column_values(eligibility, 'ML', ['Yes', 'No', ''])
    validate_column_values(eligibility, 'Include', ['Yes', 'No'])

    # Find possible inconsistencies within the file.
    for row in eligibility:
        if row['Exclusion'] != '' and row['Include'] != 'No':
            return print_row_error('eligibility.csv', row['Id'], 'If Exclusion is filled out, Include must be No.')
        if row['Exclusion'] == '' and (row['Features/Metrics'] == 'Yes' or row['ML'] == 'Yes') and row['Include'] != 'Yes':
            return print_row_error('eligibility.csv', row['Id'], 'If Features/Metrics or ML is Yes, Include must be Yes.')
        if row['Features/Metrics'] != '' and row['ML'] != '' and row['Exclusion'] == '':
            continue
        if row['Features/Metrics'] == '' and row['ML'] == '' and row['Exclusion'] != '':
            continue
        print_row_error('eligibility.csv', row['Id'], 'Either Features/Metrics and ML must be filled out or Exclusion must be filled out.')

    # Find possible inconsistencies between eligibility and general.
    for row in eligibility:
        if row['Id'] not in general_dict:
            continue # not included
        general_row = general_dict[row['Id']]
        has_metrics = general_row['Metrics'] == 'Yes'
        has_features = general_row['# Features'] != '0' and general_row['# Features'] != '0 / 0'
        if ((row['Features/Metrics'] == 'Yes') != (has_metrics or has_features)):
            print_row_error('eligibility.csv', row['Id'], 'Features/Metrics does not match general[Metrics]/[Features].')
        if ((row['ML'] == 'Yes') != (general_row['ML'] != 'N/A')):
            print_row_error('eligibility.csv', row['Id'], 'ML does not match general[ML].')

def validate_inclusion():
    print('Validating inclusion.csv...')

    for row in inclusion:
        # databases must be ACM, Google Scholar or Web of Science
        databases = [d.strip() for d in row['Databases'].split(',')]
        if not set(databases).issubset(set([
            'ACM',
            'Google Scholar', 
            'Web of Science', 
            'Backward Citation Tracking', 
            'Forward Citation Tracking'
        ])):
            print_row_error('inclusion.csv', row['Id'], 'Invalid databases.')
        
        # Authors cannot have a comma
        if ',' in row['Authors']:
            print_row_error('inclusion.csv', row['Id'], 'Authors cannot have a comma.')

        # Keywords cannot have a comma
        if ',' in row['Keywords']:
            print_row_error('inclusion.csv', row['Id'], 'Keywords cannot have a comma.')
        
        # published in
        pub_in_format = {
            'Conference': r'(.+)?\'[0-9][0-9]: .+', # e.g. OpenSym '19: [...]
            'Journal': r'(.+)?, vol. [0-9]+' # e.g. [...], vol. 1, no. 1, pp. 1-10, 2019.
        }.get(row['Publication Type'], '.+')  
        if not re.match(pub_in_format, row['Published In']):
            print_row_error('inclusion.csv', row['Id'], 'Published In does not match the format.')

        # address is either N/A or <city>, <country>
        if row['Address'] != 'N/A':
            if len(row['Address'].split(',')) != 2:
                print_row_error('inclusion.csv', row['Id'], 'Address is not in the format <city>, <country>.')
        elif row['Publication Type'] in ['Conference', 'Book']:
            print_row_error('inclusion.csv', row['Id'], 'Address must be filled out for Conferences and Books.')
            
     
        # no element can be empty or contain newlines
        for k, v in row.items():
            if '\n' in v:
                print_row_error('inclusion.csv', row['Id'], 'Newline in column "{}".'.format(k))
            if v == '':
                print_row_error('inclusion.csv', row['Id'], 'Empty value in column "{}".'.format(k))
    
    validate_column_number(inclusion, 'Id')
    validate_column_number(inclusion, 'Year')        
    validate_column_values(inclusion, 'Publication Type', ['Journal', 'Conference', 'Book', 'Other', 'N/A'])
    validate_column_number(inclusion, 'Refs.')        
    validate_column_number(inclusion, 'Cits.')   
    validate_column_values(inclusion, 'Backward Tracked', ['Yes', 'No'])
    validate_column_values(inclusion, 'Forward Tracked', ['Yes', 'No'])

    # forward tracked and backward tracked must be Yes if Total [0, 10] is >= 4, and vice versa
    for row in inclusion:
        total = int(row['Total [0, 10]'])
        if total >= 4 and (row['Backward Tracked'] != 'Yes' or row['Forward Tracked'] != 'Yes'):
            print_row_error('inclusion.csv', row['Id'], 'Total is >= 4, but Backward Tracked or Forward Tracked is not Yes.')
        if total < 4 and (row['Backward Tracked'] == 'Yes' or row['Forward Tracked'] == 'Yes'):
            print_row_error('inclusion.csv', row['Id'], 'Total is < 4, but Backward Tracked or Forward Tracked is Yes.')

def validate_qscores():
    for row in inclusion:
        general_row = general_dict[row['Id']]
        q1 = int(row['Q1 [0, 3]'])
        q2 = int(row['Q2 [0, 3]'])
        q3 = int(row['Q3 [0, 3]'])
        q4 = int(row['Q4 [0, 1]'])

        # q1 <= q2 + q3 + q4 + 1
        if q1 > q2 + q3 + q4 + 1:
            print_row_error('inclusion.csv', row['Id'], 'Q1 is greater than the sum of Q2, Q3 and Q4 + 1.')

        # ml
        gen_algos = general_row['# Algorithms']
        num_ml = int(gen_algos) if gen_algos != 'N/A' and gen_algos != '?' else 0

        if num_ml > 6:
            correct_q2 = 3
        elif num_ml > 3:
            correct_q2 = 2
        elif num_ml > 0:
            correct_q2 = 1
        else:
            correct_q2 = 0
        
        if correct_q2 != q2:
            print_row_error('qscores.csv', row['Id'], 'Q2 does not match calculated value. (calculated: {})'.format(correct_q2))


        # how feature value is determined:
        # - if general_row['Metrics'] == 'Yes', add 1
        # - if general_row['# Features'] != '0', add the number of features
        # - q3 can be 1 if metrics = No and # features = 0 / something 

        feature_value = 0
        if general_row['Metrics'] == 'Yes':
            feature_value += 1
        collected, spotted = [int(x) for x in general_row['# Features'].split(' / ')]
        feature_value += collected

        if spotted > 0:
            feature_value = max(feature_value, 1)
        
        if feature_value > 50:
            correct_q3 = 3
        elif feature_value > 15:
            correct_q3 = 2
        elif feature_value > 0:
            correct_q3 = 1
        else:
            correct_q3 = 0

        if correct_q3 != q3:
            print_row_error('qscores.csv', row['Id'], 'Q3 does not match calculated value. (calculated: {})'.format(correct_q3))


        # languages. if N/A or ? or just english then 0. if other, then 1.
        gen_languages = [l.strip().lower() for l in general_row['Languages'].split(',')]

        if gen_languages == ['n/a'] or gen_languages == ['?'] or gen_languages == ['english']:
            correct_q4 = 0
        else:
            correct_q4 = 1
        
        if correct_q4 != q4:
            print_row_error('qscores.csv', row['Id'], 'Q4 does not match calculated value. (calculated: {})'.format(correct_q4))
        


def validate_general():
    print('Validating general.csv...')

    validate_column_number(general, 'Id')

    # # features: must be in format 'x / y', where x and y are integers, and x <= y
    for row in general:
        if re.search(r'\d+ / \d+', row['# Features']) is None:
            print_row_error('general.csv', row['Id'], '# Features must be in format "x / y"')
            return False
        x, y = [int(x) for x in row['# Features'].split(' / ')]
        if x > y:
            print_row_error('general.csv', row['Id'], '# Features: x must be <= y')
            return False

    # ml: values must be in ['CL', 'DL', 'CL + DL', 'N/A']
    validate_column_values(general, 'ML', ['CL', 'DL', 'CL + DL', 'N/A'])
  
    # ml: either all N/A or all filled out
    for row in general:
        mls = [row[h] for h in ['ML', '# Algorithms', 'Best Algorithm', 'Performance', 'Perf. Metric']]
        if all(x == 'N/A' for x in mls):
            continue
        if all(x != 'N/A' for x in mls):
            continue
        print_row_error('general.csv', row['Id'], 'ML items must either all be N/A or all be filled out.')

    # type
    for row in general:
        type = row['Type'].lower()
        if type == 'literature review':
            continue
        features = row['# Features']
        ml = row['ML']

        # to lower

        if (type.find('metric') != -1) != (row['Metrics'] == 'Yes'):
            print_row_error('general.csv', row['Id'], 'Type and Metrics do not match.')

        if (type.find('feature') != -1) != (features != '0 / 0'):
            print_row_error('general.csv', row['Id'], 'Type and # Features do not match.')

        # if type has ML, ML must have CL + DL
        if (type.find('ml') != -1):            
            if (ml != 'CL + DL'):
                print_row_error('general.csv', row['Id'], 'Type and ML (CL + DL) do not match.')
            break

        if (type.find('classical') != -1) != (ml.find('CL') != -1):
            print_row_error('general.csv', row['Id'], 'Type and ML (CL) do not match.')	

        if (type.find('dl') != -1) != (ml.find('DL') != -1):
            print_row_error('general.csv', row['Id'], 'Type and ML (DL) do not match.')


    # feature counts, compare to feature dict.
    for row in general:
        x, y = [int(x) for x in row['# Features'].split(' / ')]
        collected = len(features_dict[row['Id']]) if row['Id'] in features_dict else 0
        if x != collected:
            print_row_error('general.csv', row['Id'], '# Features does not match number of features. ({} != {})'.format(x, collected))

    # ir (collumn ir must either be ?, N/A, or a number over 1)
    for row in general:
        if row['IR'] == '?':
            continue
        if row['IR'] == 'N/A':
            continue
        if float(row['IR'].replace(',', '.')) < 1:
            print_row_error('general.csv', row['Id'], 'IR must be either ?, N/A, or a number over 1.')
    return       

def is_sorted(list_of_strings):
    # By Github Copilot
    return all(int(x) <= int(y) for x, y in zip(list_of_strings, list_of_strings[1:]))
    

def validate_features():
    print('Validating features.csv...')
    validate_column_values(features, 'Category', ['Content', 'Style', 'Readability', 'History', 'Network', 'Popularity'])
    validate_column_values(features, 'Actionable', ['Yes', 'No'])
    validate_column_values(features, 'Multilingual', ['Yes', 'No'])

    # find any duplicate feature ids.
    ids = [f['Id'] for f in features]
    duplicates = [x for x in ids if ids.count(x) > 1]
    if len(duplicates) > 0:
        print('Duplicate IDs found: {}'.format(set(duplicates)))
        return False
    
    for feature in features:
        if feature['Papers'] == '':
            continue
        papers = [p.strip() for p in feature['Papers'].split(',')]

        # check that paper ids don't have duplicates and are sorted by value
        if len(papers) != len(set(papers)):
            return print_row_error('features.csv', feature['Id'], 'Duplicate papers found.')
        if not is_sorted(papers):
            return print_row_error('features.csv', feature['Id'], 'Papers are not sorted.')
        
        # check that papers are in general.csv
        for paper in papers:
            if paper not in [p['Id'] for p in general]:
                return print_row_error('features.csv', feature['Id'], 'Paper {} not found in general.csv. Was in feature {}.'.format(paper, feature['Id']))

    return True

def validate_papers():
    print('Validating papers...')
    eli = [p['Id'] for p in eligibility if p['Include'] == 'Yes']
    incl = [p['Id'] for p in inclusion]
    gen = [p['Id'] for p in general]

    # papers in the three sets must be the same
    if set(eli) != set(incl) or set(eli) != set(gen):
        print('Papers in eligibility and inclusion must be the same. Lengths: {}, {}, {}'.format(len(eli), len(incl), len(gen)))
        return False
    
def validate_sorted():
    # all id columns of eligility, inclusion, general must be sorted
    print('Validating sorted...')

    # if not sorted print index
    for variable_name, table in [('eligibility', eligibility), ('inclusion', inclusion), ('general', general)]:
        if not is_sorted([row['Id'] for row in table]):
            print('Table {} is not sorted.'.format(variable_name))
            return False
        

validate_eligibility()
validate_inclusion()
validate_qscores()
validate_general()
validate_features()
validate_papers()
validate_sorted()
print('Done.')

# print(len(features_dict['36']))

# for each item in feature dict, list paper id, name and # features
# for paper in general:
    # print paper id, title (truncated to 10 chars), # features
    # print in a table format
    # print(paper['Id'], paper['Title'][:50] + "...", len(features_dict[paper['Id']]) if paper['Id'] in features_dict else 0, sep='\t')

