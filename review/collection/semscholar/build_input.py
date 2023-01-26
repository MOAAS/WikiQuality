import json
from api import search_query

articles = json.load(open('databases/all/output.json', 'r', encoding='utf-8'))

# this obtains most ids from the database, to build the input.json file
# not found items will need to be manually searched for
# that process was conducted by searching the title through the semantic scholar website, which somehow returns results not shown by the api

complete = []
for article in articles:    
    title = article['title']    
    print("Searching for: " + title)


    info = {
        'id': article['id'],
        'original': article,
    }

    # reduce some calls to the api. if it already exists, the paperId is the same (we will remove duplicates later)
    found = next((x for x in complete if x['original']['title'] == title), None)
    if found is not None:
        complete.append({ **info, 'semscholarId': found['semscholarId'] })
        continue

    result = search_query(title)

    if result is None:
        print("Did not find above article.")
        complete.append({**info, 'semscholarId': 'not_found'})
    else:
        # extract info
        complete.append({
            **info,
            'semscholarId': result['paperId'],
        })

# dump in file
with open('semscholar/input.json', 'w', encoding='utf-8') as outfile:
    json.dump(complete, outfile, indent=4)
