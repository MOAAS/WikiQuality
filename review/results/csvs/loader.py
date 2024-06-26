import csv

def read_csv(file):
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        keys = next(reader)
        return [{k: v for k, v in zip(keys, row)} for row in reader]

titles = read_csv('filtering/titles.input.csv')
abstracts = read_csv('filtering/abstracts.input.csv')
fulltexts = read_csv('filtering/fulltexts.input.csv')

eligibility = read_csv('results/csvs/eligibility.csv') # same as fulltexts, should be at least
inclusion = read_csv('results/csvs/inclusion.csv')
general = read_csv('results/csvs/general.csv')
features = read_csv('results/csvs/features.csv')

def load_venues_into_inclusion(inclusion):
    inclusion = [dict(paper) for paper in inclusion]
    for paper in inclusion:
        venue = { 
            'Type': paper['Publication Type'],
            'Address': paper['Address'],
            'Publisher': paper['Publisher']
        }
        if (paper['Publication Type'] == "Book"):
            venue['Venue'] = paper['Published In']
            venue['Id'] = venue['Venue']
            venue['Name'] = venue['Venue']
        elif (paper['Publication Type'] == "Conference"):
            venue['Venue'] = paper['Published In'].split(',')[0]
            venue['Id'] = venue['Venue'].split(" '")[0]
            venue['Name'] = venue['Venue'].split(":", 1)[1].strip()

            if 'pp.' in paper['Published In']:
                venue['Pages'] = paper['Published In'].split('pp.')[1].strip()
        elif (paper['Publication Type'] == "Journal"):
            venue['Venue'] = paper['Published In'].split(',')[0]
            venue['Id'] = venue['Venue']
            venue['Name'] = venue['Venue']

            if 'vol.' in paper['Published In']:
                volume_part = paper['Published In'].split('vol.')[1].split(',')[0]
                venue['Volume'] = volume_part.split('(')[0].strip()
                if '(' in volume_part:
                    venue['Issue'] = volume_part.split('(')[1].split(')')[0].strip()
                
            if 'pp.' in paper['Published In']:
                venue['Pages'] = paper['Published In'].split('pp.')[1].strip()
        elif (paper['Publication Type'] == "Other"):
            venue['Venue'] = paper['Published In']
            venue['Id'] = venue['Venue'].split(':')[0].split(" '")[0]
            venue['Name'] = venue['Venue']
        elif (paper['Publication Type'] == "N/A"):
            venue['Venue'] = paper['Published In']
            venue['Id'] = venue['Venue']
            venue['Name'] = venue['Venue']
        else: 
            raise "Unknown publication type: " + paper['Publication Type']
        
        paper['Venue'] = venue
    
    return inclusion

def load_bibtex_id_into_inclusion(inclusion):
    import unicodedata
    inclusion = [dict(paper) for paper in inclusion]
    for paper in inclusion:
        paper['Bibtex'] = paper['Authors'].split(';')[0].split(' ')[-1] + paper['Year'] + "_lr" + paper['Id']

        # Remove accents, etc.
        paper['Bibtex'] = unicodedata.normalize('NFKD', paper['Bibtex']).encode('ascii', 'ignore').decode('utf-8')

    return inclusion

def join_inclusion_with_general(inclusion, general):
    inclusion = [dict(paper) for paper in inclusion]
    general = [dict(paper) for paper in general]
    for paper in inclusion:
        paper['General'] = [g for g in general if g['Id'] == paper['Id']][0]
    return inclusion

inclusion_but_with_more = load_venues_into_inclusion(inclusion)
inclusion_but_with_more = load_bibtex_id_into_inclusion(inclusion_but_with_more)
inclusion_but_with_more = join_inclusion_with_general(inclusion_but_with_more, general)

inclusion_but_as_dict = {p['Id']: p for p in inclusion_but_with_more}


def parse_paper_type(paper_general):
    if 'DL' in paper_general['ML']:
        return 'DL'
    elif 'CL' in paper_general['ML']:
        return 'CL'
    elif 'metric-based' in paper_general['Type']:
        return 'MB'
    elif 'features + correlates' in paper_general['Type'] or 'metrics + correlates' in paper_general['Type']:
        return 'FMC'
    else:
        return 'Other'

def get_feature_info(paper_id):
    categories = set()
    used_features = []
    for feature in features:
        if paper_id in feature['Papers'].split(', '):
            categories.add(feature['Category'])
            used_features.append(feature)
    
    # sort category. Content before Style before Readability before History before Network before Popularity
    custom_order = ['Content', 'Style', 'Readability', 'History', 'Network', 'Popularity']
    categories = sorted(categories, key=lambda c: custom_order.index(c) if c in custom_order else 999)
    return {
        'Categories': list(categories),
        'CategoriesShort': ''.join([c[0] for c in list(categories)]),    
        'Features': used_features
    }