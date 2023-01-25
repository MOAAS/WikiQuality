def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def dump_json(articles, filename):
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def dump_articles(articles):
    if len(articles) == 0:
        return

    # some extra processing common to all databases
    for article in articles:
        journal = article['journal'].lower()
        conference_keywords = ['conference', 'workshop', 'symposium', 'proceedings', 'meeting']
        journal_keywords = ['journal']
        if any(keyword in journal for keyword in conference_keywords):
            article['journal_type'] = 'Conference'
        elif any(keyword in journal for keyword in journal_keywords):
            article['journal_type'] = 'Journal'
        else:
            article['journal_type'] = 'unknown'

    # find duplicates
    visited = set()
    for article in articles:
        if article['title'] in visited:
            article['duplicate_of'] = next(a['id'] for a in articles if a['title'] == article['title'])
        else:
            visited.add(article['title'])


    # print json
    dump_json(articles, "all/output.json")

    # print csv
    import csv
    keys = ['id', 'database', 'title', 'authors', 'year', 'journal_type', 'journal', 'citations', 'url', 'pdf']
    with open("all/output.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for article in articles:
            writer.writerow([article[key] for key in keys])

    # print one column (if needed, for debugging)
    with open("all/output.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(article.get('title', '') for article in articles))
    print("Dumped", len(articles), "articles")



all_articles = []

from scholar.parser import parse_scholar_htmls
scholar = read_file("scholar/input.html")
scholar_articles = parse_scholar_htmls(scholar)
dump_json(scholar_articles, "scholar/output.json")
all_articles += scholar_articles

from acm.parser import parse_acm_htmls
acm = read_file("acm/input.html")
acm_articles = parse_acm_htmls(acm, all_articles[-1]['id'] + 1)
dump_json(acm_articles, "acm/output.json")
all_articles += acm_articles

from wos.parser import parse_wos_htmls
wos = read_file("wos/input.html")
wos_articles = parse_wos_htmls(wos, all_articles[-1]['id'] + 1)
dump_json(wos_articles, "wos/output.json")
all_articles += wos_articles



dump_articles(all_articles)