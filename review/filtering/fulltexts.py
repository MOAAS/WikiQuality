import csv
import json

with open('semscholar/papers.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)
    articles = {int(a['id']): a for a in articles}

with open('filtering/abstracts.input.csv', 'r', encoding='utf-8') as f:
    abstracts = csv.reader(f)  
    next(abstracts)
    abstracts = {int(a[0]): a[2] for a in abstracts}

included = []

with open('filtering/fulltexts.input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    included_col = 7
    for row in reader:
        row = [r for r in row]
        if row[included_col].lower() == 'yes':
            id = int(row[0])
            article = articles[id]
            if (article['semscholarId'] == 'not_found'):
                included.append({
                    'id': id,
                    'databases': ', '.join(article['databases']),
                })
            else:
                included.append({
                    'id': id,
                    'databases': ', '.join(article['databases']),
                    'title': row[1],

                    'year': article['year'],
                    'authors': article['authors'],
                    'publication_type': article['publication_type'],
                    'published_in': article['published_in'],
                    'num_references': article['num_references'],
                    'num_citations': article['num_citations'],
                    'abstract': abstracts[id],
                    'keywords': '',
                    'pdf': row[3],
                    'url': row[2],
                })


keys = [
    'id', 'databases', 'title',
    'year', 'authors', 'publication_type', 'published_in', 'num_references', 'num_citations', 'abstract', 'keywords', 'pdf', 'url',
]
with open("filtering/fulltexts.output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for row in included:
        for key in keys:
            if key not in row:
                row[key] = ''
        writer.writerow([row[key] for key in keys])
        
print("Included " + str(len(included)) + " articles.")