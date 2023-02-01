import json
import csv

with open('semscholar/papers.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

included_ids = set()
with open('filtering/titles.input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    included_col = 4
    for row in reader:
        row = [r.lower() for r in row]
        if row[included_col] == 'yes' or row[included_col] == 'maybe':
            included_ids.add(int(row[0]))

keys = [
    'id', 'databases', 'title', 'abstract', 'authors', 'year', 'publication_type', 'published_in',
    'num_references', 'num_citations', 'url', 'doi', 'pdf'
]
with open("filtering/titles.output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for article in articles:
        if article['id'] not in included_ids:
            continue
        if 'databases' in article:
            article['databases'] = ', '.join(article['databases'])
        for key in keys:
            if key not in article:
                article[key] = ''
        writer.writerow([article[key] for key in keys])
