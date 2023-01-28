import csv

included_ids = set()
with open('filtering/abstracts.input.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        row = [r.lower() for r in row]
        if row[1] == 'yes' or row[1] == 'maybe':
            included_ids.add(int(row[0]))

keys = [
    'id'
]
with open("filtering/abstracts.output.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for id in included_ids:
        writer.writerow([id])
        
print("Included " + str(len(included_ids)) + " articles.")