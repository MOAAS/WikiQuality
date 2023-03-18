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
