import csv

included = []
with open('filtering/abstracts.input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        row = [r for r in row]
        if row[4].lower() == 'yes' or row[4].lower() == 'maybe':
            included.append({
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'pdf': row[3]
            })


keys = [
    'id', 'title', 'url', 'pdf'
]
with open("filtering/abstracts.output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for row in included:
        writer.writerow([row[k] for k in keys])
        
print("Included " + str(len(included)) + " articles.")