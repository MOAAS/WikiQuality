BASE_URL = "https://dl.acm.org"
def parse_acm_htmls(html, startId=1):
    from bs4 import BeautifulSoup
    all_articles = []

    soup = BeautifulSoup(html, 'html.parser')

    # get all html documents
    htmls = soup.find_all('html')
    id = startId
    for html in htmls:
        results = html.find(class_='items-results')
        articles = results.find_all('div', class_='issue-item')

        for article in articles:
            all_articles.append(extract_info(article, id))
            id += 1

    return all_articles

def extract_info(article, id):
    title_anchor = article.find(class_='issue-item__title').find('a')

    title = title_anchor.text
    url = BASE_URL + title_anchor['href']
   
    author_lis = article.find('ul', attrs={'aria-label': 'authors'}).find_all('li')
    authors = [author.find('a').attrs['title'] for author in author_lis]
    
    date = article.find(class_='bookPubDate').attrs['data-title'].split(': ')[-1]
    year = date.split(' ')[-1]
    num_citations = article.find(class_='metric-holder').find(class_='citation').find('span').text

    type = article.find(class_='issue-item__citation').find(class_='issue-heading').text.replace('-', ' ')
    type = type[0].upper() + type[1:].lower() # capitalize first letter of string

    return {
        'id': id,
        'database': 'ACM',
        'title': title,
        'authors': ', '.join(authors),
        'year': year,
        'journal': find_journal(article),
        'citations': int(num_citations),
        'url': url,
        'pdf': find_pdf(article),

        'type': type,
        'date': date,
    }

def find_journal(article):
    details = article.find(class_='issue-item__detail')
    if details is None:
        return 'N/A'
    journal = details.find('a').text
   
    info = details.find(class_='dot-separator').text.replace('–', '-')
    return journal + ", " + info
    


def find_pdf(article):
    anchor = article.find('a', attrs={'aria-label': 'Get Access'})
    if anchor is None:
        return 'N/A'
    return BASE_URL + anchor['href']
    
    