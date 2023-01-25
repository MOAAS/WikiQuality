import re

BASE_URL = "https://www.webofscience.com/"

def parse_wos_htmls(html, startId=1):
    from bs4 import BeautifulSoup
    all_articles = []

    soup = BeautifulSoup(html, 'html.parser')

    # get all html documents
    htmls = soup.find_all('html')
    id = startId
    for html in htmls:
        results = html.find(class_='app-records-list')
        articles = results.find_all('div', class_='summary-record')

        for article in articles:
            all_articles.append(extract_info(article, id))
            id += 1

    return all_articles


def extract_info(article, id):
    title_anchor = article.find(class_='title-link')

    title = title_anchor.text
    url = BASE_URL + title_anchor['href']
   
    author_anchors = article.find('app-summary-authors').find_all(class_='authors')
    authors = [author.text for author in author_anchors]
    
    year_span = article.find('span', attrs={'name': 'pubdate'})

   
    date = article.find('span', attrs={'name': 'pubdate'}).text.replace('|', '').strip()
    year = re.search(r'\d{4}', year_span.text).group()  # find 4 digit year

    return {
        'id': id,
        'database': 'Web of Science',
        'title': title,
        'authors': '; '.join(authors),
        'year': year,
        'journal': find_journal(article),
        'citations': find_citations(article),
        'url': url,
        'pdf': find_pdf(article),

        'date': date,
    }

def find_citations(article):
    citations = article.find('div', class_='stats-section-section').find(attrs={'data-ta': 'stat-number-citation-related-count'})
    if citations is None:
        return 0
    else:
        citations = citations.text.strip()
        if citations == '':
            return 0
        else:
            return int(citations)

def find_pdf(article):    
    links = article.find('app-summary-record-links').find_all('a')
    for link in links:
        if 'full text' in link.text.lower():
            return BASE_URL + link['href']
    return 'N/A'
    
def find_journal(article):
    journal = article.find('a', attrs={'cdxanalyticscategory': 'wos-recordCard_Journal_Info'})
    conference = article.find('a', attrs={'data-ta': 'Summary-conferenceName'})

    pages = article.find(attrs={'data-ta': 'Summary-page-no'})
    volume = article.find(attrs={'data-ta': 'Summary-volume'})
    issue = article.find(attrs={'data-ta': 'Summary-issue'})

    rest = []
    if volume is not None:
        rest.append(volume.text.strip())
    if issue is not None:
        rest.append(issue.text.strip())
    if pages is not None:
        rest.append(pages.text.strip())
    # get the parent of page, volume or issue, any that is not None
   # info = next((p for p in [pages, volume, issue] if p is not None), None)
    #rest = "" if info is None else info.parent.text

    rest = ' '.join(rest)
    
    if journal is not None:

        return journal.text + " " + rest
    elif conference is not None:
        return conference.text + " " + rest
    else:
        return 'N/A'

