import json
from api import search_query

# this obtains most ids from the database, to build the input.json file
# not found items will need to be manually searched for
# that process was conducted by searching the title through the semantic scholar website, which somehow returns results not shown by the api

# potentially wrong results are also marked. 
# that issue will also be dealt with manually, by comparing the result with the original article

# still, there are times when the api has more than one version of the paper, but returns a result that is less complete.
# for these reasons, it is better not to run this script again. it was good for building a starting point, though.

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


articles = json.load(open('databases/all/output.json', 'r', encoding='utf-8'))
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
        if similar(title.lower(), result['title'].lower()) < 0.8:
            info['possibly_wrong_result'] = True
        # extract info
        complete.append({
            **info,
            'semscholarId': result['paperId'],
        })

# dump in file
with open('semscholar/ids.json', 'w', encoding='utf-8') as outfile:
    json.dump(complete, outfile, indent=4)
