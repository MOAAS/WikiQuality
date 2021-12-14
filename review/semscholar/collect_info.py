import re
import json
from api import search_multiple

articles = json.load(open('semscholar/ids.json', 'r', encoding='utf-8'))

def validate_input(articles):
    # check all object that have key "possibly_wrong_result" and set to True
    invalid = [a for a in articles if 'possibly_wrong_result' in a and a['possibly_wrong_result'] == True]
    if len(invalid) > 0:
        print("Found " + str(len(invalid)) + " possibly wrong results. Please check them manually.")
        exit()

def assign_duplicates(articles):
    articles = [a for a in articles if a['semscholarId'] != 'not_found']
   
    visited = set()
    for article in articles:
        if article['semscholarId'] in visited:
            # find first article with same id. no need to optimize, not that many articles
            for a in articles: 
                if 'semscholarId' in a and a['semscholarId'] == article['semscholarId']:
                    article['duplicate_of'] = a['id']
                    break

            # delete every property but id, original and duplicate_of
            for key in list(article.keys()):
                if key not in ['id', 'original', 'duplicate_of']:
                    del article[key]
        else:
            visited.add(article['semscholarId'])

def extract_info(paper):      
    def extract_pub_type():
        if paper['publicationVenue'] is not None and 'type' in paper['publicationVenue']:
            return paper['publicationVenue']['type']

        if paper['publicationTypes'] is not None and 'Conference' in paper['publicationTypes']:
            return 'conference'

        if paper['journal'] is not None:
            name = paper['journal'].get('name', '').lower()
            if 'conference' in name or 'proceedings' in name or 'workshop' in name or 'symposium' in name:
                return 'conference'
            
            # if it has a volume, it is a journal
            if 'volume' in paper['journal']:
                return 'journal'
        
        if paper['externalIds'] is not None and 'DBLP' in paper['externalIds']:
            dblp = paper['externalIds']['DBLP']
            if 'conf' in dblp:
                return 'conference'
            if 'journal' in dblp or 'series' in dblp:
                return 'journal'
            if 'book' in dblp:
                return 'book'
            if 'phd' in dblp or 'masters' in dblp or 'thesis' in dblp:
                return 'thesis'
            
        return 'unknown'
            
    def extract_pub():
        # get name. first try journal['name'], then publicationVenue['name']
        if paper['journal'] is not None and 'name' in paper['journal'] and paper['journal']['name'] is not None and paper['journal']['name'] != '':
            str = paper['journal']['name']
        elif paper['publicationVenue'] is not None:
            str = paper['publicationVenue']['name']
        else:
            return "N/A"
        
        # add volume and issue        
        if paper['journal'] is not None:
            journal = paper['journal']
            if 'volume' in journal:
                str += ', ' + journal['volume']
                if 'issue' in journal:
                    str += '(' + journal['issue'] + ')'
            if 'pages' in journal:
                str += ', pp. ' + journal['pages']
        return str
        
    if paper['title'].isupper(): # if title is in all caps, capitalize it
        paper['title'] = paper['title'].capitalize()

    # replace repeated spaces with single space + repeated newlines with single newline
    if paper['abstract'] is not None:
        paper['abstract'] = re.sub(r'\s+', ' ', paper['abstract'])
    
    return {
        'title': paper['title'],
        'abstract': paper['abstract'],
        'authors': '; '.join([a['name'] for a in paper['authors']]),
        'year': paper['year'],
        'publication_type': extract_pub_type().capitalize(),
        'published_in': extract_pub(),
        'num_references': paper['referenceCount'],
        'num_citations': paper['citationCount'],
        'url': paper['url'],
        'doi': paper['externalIds']['DOI'] if 'DOI' in paper['externalIds'] else None,
        'pdf': paper['openAccessPdf']['url'] if paper['openAccessPdf'] is not None else None,
        #'paper': paper
    }

def fill_article_info(articles):
    ids = [a['semscholarId'] for a in articles if 'semscholarId' in a and a['semscholarId'] != 'not_found']
    papers = search_multiple(ids)
    papers = {p['paperId']: p for p in papers} # make it a dict for easier access
    # with open('semscholar/papers.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(papers, outfile, indent=4)

    for article in articles:
        if 'semscholarId' in article and article['semscholarId'] != 'not_found':
            info = extract_info(papers[article['semscholarId']])
            article.update(info)
        
    print("Found " + str(len(papers)) + " papers. From " + str(len(ids)) + " ids.")

    
def fill_article_databases(articles):
    for article in articles:
        if 'duplicate_of' in article:
            duped = next((a for a in articles if a['id'] == article['duplicate_of']), None)
            duped['databases'].append(article['original']['database'])
        else:
            article['databases'] = [article['original']['database']]
            continue

    # remove duplicate databases + sort them
    for article in articles: 
        if 'databases' in article: 
            article['databases'] = sorted(list(set(article['databases'])))
    

def reorder_keys(articles):
    # rename and order keys to match our needs
    for article in articles:
        if 'duplicate_of' in article or article['semscholarId'] == 'not_found':
            article['original'] = article.pop('original') # move original to end 
            continue
        else:
            keys = list(article.keys())
            keys.remove('id')
            keys.remove('semscholarId')
            keys.remove('original')
            keys = ['id', 'semscholarId'] + keys + ['original']
            ordered_article = {k: article[k] for k in keys}
            article.clear()
            article.update(ordered_article)

validate_input(articles)
assign_duplicates(articles)
fill_article_databases(articles)
fill_article_info(articles)
reorder_keys(articles)

with open('semscholar/papers.json', 'w', encoding='utf-8') as outfile:
    json.dump(articles, outfile, indent=4)

print("Dumped " + str(len(articles)) + " articles to semscholar/papers.json")