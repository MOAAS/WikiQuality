import requests

#### WIKIPEDIA API ####

WIKI_API_URL = 'https://en.wikipedia.org/w/api.php?formatversion=2&format=json'
headers = {
    'User-Agent': 'WikiQualityDatasetCollector/1.0 (up201705208@edu.fe.up.pt)',
}

def encodeToURL(title):
    # replace spaces with underscores and & with %26
    return title.replace(' ', '_').replace('&', '%26')

def getWikiPageText(title):    
    url = f'{WIKI_API_URL}&action=parse&page={encodeToURL(title)}&prop=wikitext|sections'

    res = requests.get(url, headers=headers).json()        

    if 'error' in res:
        print(f'Error while fetching page ({title}): {res["error"]["info"]}')
        return ''
        
    return res['parse']['wikitext']

def getWikiPages(titles):
    url = f'{WIKI_API_URL}&action=query&prop=revisions&titles={encodeToURL(titles)}&rvprop=content&rvslots=*'

    res = requests.get(url, headers=headers).json()
    pages = res['query']['pages']

    # get page text
    pageText = {}
    for page in pages:
        pageText[page['title']] = page['revisions'][0]['slots']['main']['content']

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