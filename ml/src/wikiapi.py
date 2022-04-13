import requests

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
    
    i = 0
    while i < len(titles):
        if (i % 100 == 0):
            print(f'Retrieving {len(titles)} pages... {i}/{len(titles)}')
        pages.update(getMultiWikiTextHelper(titles[i:i+50]))
        i += 50

    if (len(titles) != len(pages)):
        print(f'Warning: A total of {len(titles) - len(pages)} titles were not found in the wiki')
    
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
    }).json()

    if 'error' in res:
        print(f'Error while fetching pages ({titles}): {res["error"]["info"]}')
        return ''


    pages = res['query']['pages']
    pageText = {}
    for page in pages:
        if 'missing' in page:
            print('Error while fetching page (' + page['title'] + '): Missing page')
            continue
        wikitext = page['revisions'][0]['slots']['main']['content']

        # if wikitext has #REDIRECT
        if wikitext.lower().startswith('#redirect'):
            # from #REDIRECT [[X]], find X
            redirect = wikitext.split('[[')[1].split(']]')[0].split('|')[0].split('#')[0]
            print('Reading wikitext for: ' + page['title'] + '... Found redirect to: ' + redirect)
            wikitext = getWikiText(redirect)

        pageText[page['title']] = wikitext

    return pageText

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
    return revs