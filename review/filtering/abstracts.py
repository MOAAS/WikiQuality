import csv

included = []
with open('filtering/abstracts.input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    included_col = 4
    for row in reader:
        row = [r for r in row]
        if row[included_col].lower() == 'yes' or row[included_col].lower() == 'maybe':
            included.append({
                'Id': row[0],
                'Title': row[1],
                'Url': row[3],
            })


keys = [
    'Id', 'Title', 'Url'
]
with open("filtering/abstracts.output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for row in included:
        writer.writerow([row[k] for k in keys])
        
print("Included " + str(len(included)) + " articles.")