
def parse_scholar_htmls(html, startId=1):
    from bs4 import BeautifulSoup
    all_articles = []

    soup = BeautifulSoup(html, 'html.parser')

    # get all html documents
    htmls = soup.find_all('html')
    id = startId
    for html in htmls:
        results = html.find(id='gs_res_ccl_mid')
        articles = results.find_all('div', class_='gs_r gs_or gs_scl')
        for article in articles:
            all_articles.append(extract_info(article, id))
            id += 1            
    return all_articles

def extract_info(article, id):
    h3 = article.find('h3', class_='gs_rt')
    anchor = h3.find('a')
    title = h3.text if anchor is None else anchor.text
    url = 'N/A' if anchor is None else anchor['href']
   
    info = article.find('div', class_='gs_a').text.split(' - ')
    authors = info[0] if len(info) > 1 else 'N/A'
    journal = info[1] if len(info) > 2 else 'N/A'

    other = article.find('span', class_='gs_ct1')
   
    return {
        'id': id,
        'database': 'Google Scholar',
        'title': title,
        'url': url,
        'authors': authors,
        'year': find_year(journal),
        'journal': journal,
        'citations': find_num_citations(article),
        'pdf': find_pdf(article),
       
        'other_info': "" if other is None else other.text[1:-1]
    }


def find_pdf(article):
    aside = article.find('div', class_='gs_ggs gs_fl')
    if aside is None:
        return 'N/A'
    pdf_anchor = aside.find('a')
    if pdf_anchor is None or 'PDF' not in pdf_anchor.text:
        return 'N/A'
    return pdf_anchor['href']

def find_num_citations(article):
    bottom_anchors = article.find('div', class_='gs_ri').find('div', class_='gs_fl').find_all('a')
    for anchor in bottom_anchors:
        if 'Cited by' in anchor.text:
            return int(anchor.text.split(' ')[2])
    return '0'


import re
def find_year(journal):
    if journal == 'N/A':
        return 'N/A'
  
    # find first four digits
    match = re.search(r'\d{4}', journal)
    if match is None:
        return 'N/A'
    return int(match.group(0))