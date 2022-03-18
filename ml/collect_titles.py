from bs4 import BeautifulSoup
import requests

import wikiapi


# soup open url
def getSoup(url):
    html = getHTML(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getHTML(url):
    r = requests.get(url)
    return r.content

def getWikiQualityPages(category, filename, isPageList = False):
    members = wikiapi.getWikiCategoryMembers(category)
    
    # open file and write titles
    with open(filename, 'w', encoding='utf-8') as f:        
        # Most classes do not have page lists, just category lists, so we have a different behavior for each case
        # Could do first case for every class, but it is much slower and start/stub would take forever
        if (isPageList):
            print(f'Writing All Articles: {len(members)} pages')
            f.write('\n'.join(members + [""])) 
        else:      
            for i, subcategory in enumerate(members):                
                subMembers = wikiapi.getWikiCategoryMembers(subcategory)  
                print(f'Current Subcategory: {subcategory} - {len(subMembers)} members ({i+1}/{len(members)})')
                titles = [member for member in subMembers if member.startswith('Talk:')] # must start with "Talk:", because we don't want other subcategories
                f.write('\n'.join(titles + [""])) # '+ [""]' because we also want a \n after the last title
    
    print("Removing duplicates and cleaning titles")
    with open(filename, 'r', encoding='utf-8') as f:
        titles = f.read().split('\n')        
        titles = [title for title in titles if title != ''] # remove empty lines (usually only last one is empty, but better safe than sorry)
        titles = list(set(titles)) # remove duplicates        
        titles = [title.replace('Talk:', '') for title in titles] # remove "Talk:"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(titles))
        

# Start Articles take the longest to collect, Stubs and Cs too
#getWikiQualityPages("Category:Featured_articles", "FA.txt", True)
#getWikiQualityPages("Category:FL-Class_articles", "FL.txt")
#getWikiQualityPages("Category:A-Class_articles", "A.txt")
getWikiQualityPages("Category:Wikipedia_good_articles", "GA.txt")
#getWikiQualityPages("Category:B-Class_articles", "B.txt")
#getWikiQualityPages("Category:C-Class_articles", "C.txt")
#getWikiQualityPages("Category:Start-Class_articles", "Start.txt")
#getWikiQualityPages("Category:All_stub_articles", "Stub.txt", True)



# print(getHTML("https://en.wikipedia.org/wiki/Category:FA-Class_articles"))




