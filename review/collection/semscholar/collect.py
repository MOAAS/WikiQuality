import json
from api import search_multiple

articles = json.load(open('semscholar/input.json', 'r', encoding='utf-8'))

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

def fill_article_info(articles):
    ids = [a['semscholarId'] for a in articles if 'semscholarId' in a and a['semscholarId'] != 'not_found']
    papers = search_multiple(ids)
    papers = {p['paperId']: p for p in papers} # make it a dict for easier access
    # with open('semscholar/papers.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(papers, outfile, indent=4)

    def extract_info(paper):
        return {
            'title': paper['title'],
            'abstract': paper['abstract'],
        }

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

    for article in articles:
        if 'databases' in article:
            article['databases'] = list(set(article['databases']))
    

def reorder_keys(articles):
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

with open('semscholar/output.json', 'w', encoding='utf-8') as outfile:
    json.dump(articles, outfile, indent=4)

import csv
keys = ['id', 'title', 'databases', 'duplicate_of']
with open("semscholar/output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for article in articles:
        if 'databases' in article:
            article['databases'] = ','.join(article['databases'])
        for key in keys:
            if key not in article:
                article[key] = ''
        writer.writerow([article[key] for key in keys])
