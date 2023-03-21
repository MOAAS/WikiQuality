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
        venue = { 'Type': paper['Publication Type'] }
        if (paper['Publication Type'] == "Book" or paper['Publication Type'] == "N/A"):
            venue['Venue'] = paper['Published In']
            venue['Id'] = venue['Venue']
            venue['Name'] = venue['Venue']
        elif (paper['Publication Type'] == "Conference"):
            venue['Venue'] = paper['Published In'].split(',')[0]
            venue['Id'] = venue['Venue'].split(" '")[0]
            venue['Name'] = venue['Venue'].split(":", 1)[1].strip()
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

        
inclusion_but_with_more = load_venues_into_inclusion(inclusion)
inclusion_but_with_more = load_bibtex_id_into_inclusion(inclusion_but_with_more)