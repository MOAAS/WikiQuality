import requests

#### WIKIPEDIA API ####

WIKI_API_URL = 'https://en.wikipedia.org/w/api.php?formatversion=2&format=json'
headers = {
    'User-Agent': 'WikiQualityDatasetCollector/1.0 (up201705208@edu.fe.up.pt)',
}

def encodeToURL(title):
    # replace spaces with underscores and & with %26
    return title.replace(' ', '_').replace('&', '%26')

#def getWikiText(title):    
#    res = requests.get(WIKI_API_URL, headers=headers, params={
#        'action': 'parse',
#        'page': title,
#        'prop': 'wikitext|sections',
#        'explaintext': 'True',
#        'exsectionformat': 'plain',
#    }).json()     
#
#    if 'error' in res:
#        print(f'Error while fetching page ({title}): {res["error"]["info"]}')
#        return ''
#        
#    return res['parse']['wikitext']

def getPlainText(title):
    return getMultiPlainText([title])[title]

def getMultiPlainText(titles):
    titles = '|'.join(titles)
    res = requests.get(WIKI_API_URL, headers=headers, params={
        'action': 'query',
        'titles': titles,
        'prop': 'extracts',
        'explaintext': 'True',
        'exsectionformat': 'plain',
    }).json()

    if 'error' in res:
        print(f'Error while fetching pages ({titles}): {res["error"]["info"]}')
        return ''

    pages = res['query']['pages']
    pageText = {}
    for page in pages:
        pageText[page['title']] = page['extract']
        
    return pageText


def getWikiText(title):
    return getMultiWikiText([title])[title]

def getMultiWikiText(titles):
    pages = {}
    
    i = 0
    while i < len(titles):
        print(f'Retrieving {len(titles)} pages... {i}/{len(titles)}')
        pages.update(getMultiWikiTextMax50(titles[i:i+50]))
        i += 50
    
    print(f'Retrieved {len(titles)} pages.')

    return pages

def getMultiWikiTextMax50(titles):
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
            pageText[page['title']] = None
            continue
        wikitext = page['revisions'][0]['slots']['main']['content']

        # if wikitext has #REDIRECT
        if wikitext.startswith('#REDIRECT'):
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