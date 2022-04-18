import requests
from datetime import datetime

WIKI_API_URL = 'https://en.wikipedia.org/w/api.php?formatversion=2&format=json'
headers = {
    'User-Agent': 'WikiQualityDatasetCollector/1.0 (up201705208@edu.fe.up.pt)',
}

def getWikiText(title):
    res = getMultiWikiText([title])

    # if 0 keys
    if len(res) == 0:
        return ""
    # return the only item in the dictionary. using res[title] does not always work,
    # because the title may be formatted slightly differently. this ensures that this call never fails
    return res[list(res.keys())[0]]

def getMultiWikiText(titles):
    pages = {}
    
    for i in range(0, len(titles), 50):
        if (len(titles) > 1 and i % 250 == 0):
            print(f'Retrieving {len(titles)} pages... {i}/{len(titles)}')
        pages.update(getMultiWikiTextHelper(titles[i:i+50]))

    if (len(titles) != len(pages)):
        print(f'Warning: A total of {len(titles) - len(pages)} titles were not found in the wiki')
    
    if (len(titles) > 1):
        print(f'Retrieving {len(titles)} pages... {len(titles)}/{len(titles)}')

    return pages

def getMultiWikiTextHelper(titles):
    assert len(titles) <= 50

    titles = '|'.join(titles)
    res = requests.get(WIKI_API_URL, headers=headers, params={
        'action': 'query',
        'titles': titles,
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': '*',    
        'redirects': 1,
    }).json()

    if 'error' in res:
        print(f'Error while fetching pages ({titles}): {res["error"]["info"]}')
        return ''

    pages = res['query']['pages']
    wikitexts = {}
    for page in pages:
        if 'missing' in page:
            print('Error while fetching page (' + page['title'] + '): Missing page')
            continue
        wikitext = page['revisions'][0]['slots']['main']['content']
        wikitexts[page['title']] = wikitext

    return wikitexts

def getWikiCategoryMembers(category):
    if not category.startswith('Category:'):
        print(f"Warning: Input invalid category name ({category})")
        return []

    url = f'{WIKI_API_URL}&action=query&list=categorymembers&cmtitle={category}&cmlimit=500'
    res = requests.get(url, headers=headers).json()
    titles = [page['title'] for page in res['query']['categorymembers']]

    # while response has continue
    pageNum = 1
    while 'continue' in res:
        if (pageNum % 10 == 0):
            print(f'Retrieving {category}: {len(titles)} titles collected')
        res = requests.get(url + '&cmcontinue=' + res['continue']['cmcontinue']).json()
        titles += [page['title'] for page in res['query']['categorymembers']]
        pageNum += 1

    return titles

def getFullHistory(title):
    params = {
        'action': 'query',
        'titles': title,
        'prop': 'revisions',
        'rvlimit': 'max',
        'rvprop': 'timestamp|user|size|ids|comment',
        'rvslots': '*',
        'redirects': 1,
    }
    res = requests.get(WIKI_API_URL, headers=headers, params=params).json()
    revs = [rev for rev in res['query']['pages'][0]['revisions']]

    if 'error' in res:
        print(f'Error while fetching page history ({title}): {res["error"]["info"]}')
        return ''

    while 'continue' in res:
        res = requests.get(WIKI_API_URL, headers=headers, params={
            **params,
            'rvcontinue': res['continue']['rvcontinue']            
        }).json()
        revs += [rev for rev in res['query']['pages'][0]['revisions']]
        
    revs = [{**r, 'age': (datetime.now() - datetime.strptime(r['timestamp'], '%Y-%m-%dT%H:%M:%SZ')).days} for r in revs]
    
    return revs

def getSingleNumTranslations(title):
    res = getNumTranslations([title])
    if len(res) == 0:
        return 0
    return res[list(res.keys())[0]] # return only item

def getNumTranslations(titles):
    pages = {}
    
    for i in range(0, len(titles), 50):
        only50titles = titles[i:i+50]
        res = requests.get(WIKI_API_URL, headers=headers, params={
            'action': 'query',
            'titles': '|'.join(only50titles),
            'prop': 'langlinkscount',
            'redirects': 1,
        }).json()

        if 'error' in res:
            print(f'Error while fetching pages ({titles}): {res["error"]["info"]}')
            return ''
        
        for page in res['query']['pages']:
            pages[page['title']] = page['langlinkscount'] if 'langlinkscount' in page else 0

    return pages

