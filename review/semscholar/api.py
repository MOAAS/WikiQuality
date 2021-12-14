# PROBLEMS WITH sscholar: 
#   author names are not always complete (only checked one case).

# Documentation:
# - https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper

import requests
import json
import time

def call_api(path, body = None, extra_headers=None):
    base_url = 'https://api.semanticscholar.org/graph/v1/'
    headers = {
        'User-Agent': "MOAAS/1.0 (mailto:up201705208@edu.fe.up.pt)",
        'Accept': "application/json",
    }
  
    if extra_headers is not None:
        headers.update(extra_headers)

    if body is not None:
        r = requests.post(base_url + path, headers=headers, json=body)
    else:
        r = requests.get(base_url + path, headers=headers)

    if r.status_code == 429:
        print("Too many requests, sleeping for 1 minute.")
        time.sleep(60)
        return call_api(path, extra_headers)
        
    if r.status_code != 200:
        print("Failed to get data from scholar API (path: " + path + ")")
        print(str(r.status_code) + " " + r.text)
        return None
    return json.loads(r.text)

# https://api.semanticscholar.org/graph/v1/paper/c6f61f344c919493886bf67d0e64e0242ae83547?fields=url,year,authors,referenceCount,externalIds

def search_doi(doi):
    # use formated string
    data = call_api(f'paper/DOI:{doi}?fields=url,year,authors,referenceCount,externalIds')
    
    with open('test.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return data

def search_id(paper_id):
    # use formated string
    data = call_api(f'paper/{paper_id}?fields=url,year,authors')
    return data

def search_multiple(paper_ids):
    fields = [
        'title', 'url', 'year', 'authors', 'abstract', 'externalIds',        
        'publicationVenue', 'publicationTypes','journal', 
        'isOpenAccess', 'openAccessPdf',
        'referenceCount', 'citationCount', 'influentialCitationCount'
    ]
    data = call_api(f'paper/batch?fields={",".join(fields)}', body={ 'ids': paper_ids})
    return data

def search_query(query):
    fields = ['title', 'url', 'externalIds']
    data = call_api(f'paper/search?query={query}&fields={",".join(fields)}&offset=0&limit=1')
        
    #print(json.dumps(data, indent=4))

    if len(data['data']) == 0:
        return None
    return data['data'][0]


# search for Wikipedia
#search_query('Predicting quality flaws in user-generated content: the case of wikipedia')

#search_doi('10.1145/1367497.1367673')
