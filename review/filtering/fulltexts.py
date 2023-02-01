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
            # something like this may be needed for citation tracking
            # if id not in articles:
            #     included.append({
            #         'Id': id,
            #         'Databases': ', '.join(row[4].split(';')),
            #     })
            article = articles[id]
            if (article['semscholarId'] == 'not_found'):
                included.append({
                    'Id': id,
                    'Databases': ', '.join(article['databases']),
                })
            else:
                included.append({
                    'Id': id,
                    'Databases': ', '.join(article['databases']),
                    'Title': row[1],

                    'Year': article['year'],
                    'Authors': article['authors'],
                    'Publication Type': article['publication_type'],
                    'Published In': article['published_in'],
                    '# References': article['num_references'],
                    '# Citations': article['num_citations'],
                    'Abstract': abstracts[id],
                    'Keywords': '',
                    'PDF': row[3],
                    'URL': row[2],
                })


keys = [
    'Id', 'Databases', 'Title',
    'Year', 'Authors', 'Publication Type', 'Published In', '# References', '# Citations', 'Abstract', 'Keywords', 'PDF', 'URL'
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