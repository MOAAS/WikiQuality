import csv

def read_csv(file):
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        keys = next(reader)
        return [{k: v for k, v in zip(keys, row)} for row in reader]
    
inclusion = read_csv('validation/inclusion.csv')

# make a dictionary of authors
authors = {}

for row in inclusion:
    # row['Authors'] is of the format 'Author1; Author2; Author3'
    for author in row['Authors'].split('; '):
        if author not in authors:
            authors[author] = []
        authors[author].append(row['Id'])

# sort authors by name
authors = {k: v for k, v in sorted(authors.items(), key=lambda item: item[0])}

with open('validation/authors.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Affiliation', 'Country', 'Papers']) # Affiliation and Country will be empty for now
    for author, papers in authors.items():
        writer.writerow([author, '', '', ', '.join(papers)])

def show_authors_with_more_than_n_papers(n):
    for author, papers in authors.items():
        if len(papers) > n:
            print(author, papers)

show_authors_with_more_than_n_papers(0)