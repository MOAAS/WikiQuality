# PROBLEMS WITH crossref: 
#   rarely has abstract,
#   titles/subtitles are weird. 
#   has less articles -> less citations
#   citation info is limited (count only)

# For now we will use semantic scholar

import requests
import json

def call_api(path, extra_headers=None):
    base_url = 'https://api.crossref.org/'
    headers = {
        'User-Agent': "MOAAS/1.0 (mailto:up201705208@edu.fe.up.pt)",
        'Accept': "application/json",
    }
  

    if extra_headers is not None:
        headers.update(extra_headers)

    r = requests.get(base_url + path, headers=headers)
    data = json.loads(r.text)

    if data['status'] != 'ok':
        print("Failed to get data from crossref API (path: " + path + ")")
        return
    return data


def search_query(query, max_items):
    data = call_api('works?query=' + query + '&rows=' + str(max_items) + '&select=DOI,title,subtitle,abstract')

    result = data['message']['items'][0]

    parsed_title = result['title'][0]
    if 'subtitle' in result:
        parsed_title += ":" + result['subtitle'][0]
    
    result['title'] = parsed_title
    
    with open('test.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

    return data

def search_doi(doi):
    data = call_api('works/' + doi)

    with open('test.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    # parsed_authors = [author['family'] + ", " + author['given'] for author in result['author']]
    # result['authors'] = parsed_authors
    # del result['author']
    return data


# search for Wikipedia
search_query('Predicting quality flaws in user-generated content: the case of wikipedia', 1)

#search_doi('10.1145/1367497.1367673')


