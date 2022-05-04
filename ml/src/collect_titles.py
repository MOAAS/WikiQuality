from enum import unique
from nbformat import write
import wikiapi
import os       


folder = os.path.join(os.path.dirname(__file__), '..', 'titles')


def getWikiQualityPages(category, filename, isPageList = False):
    members = wikiapi.getWikiCategoryMembers(category)

    path = os.path.join(folder, filename)
    
    # open file and write titles
    with open(path, 'w', encoding='utf-8') as f:        
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
    titles = getTitles(filename)
    titles = [title for title in titles if title != '' and not title.endswith('GA1')] # remove empty lines (usually only last one is empty, but better safe than sorry)       
    titles = list(set(titles)) # remove duplicates     
    titles = [title.replace('Talk:', '') for title in titles] # remove "Talk:"
    writeTitles(filename, titles)
 

def getTitles(filename):
    with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
        return f.read().split('\n')

def writeTitles(filename, titles):
    with open(os.path.join(folder, filename), 'w', encoding='utf-8') as f:
        f.write('\n'.join(titles))


# Start Articles take the longest to collect, Stubs and Cs too
getWikiQualityPages("Category:Featured_articles", "FA.txt", isPageList=True)
getWikiQualityPages("Category:FL-Class_articles", "FL.txt")
getWikiQualityPages("Category:A-Class_articles", "A.txt")
getWikiQualityPages("Category:Wikipedia_good_articles", "GA.txt")
getWikiQualityPages("Category:B-Class_articles", "B.txt")
getWikiQualityPages("Category:C-Class_articles", "C.txt")
getWikiQualityPages("Category:Start-Class_articles", "Start.txt")
getWikiQualityPages("Category:All_stub_articles", "Stub.txt", isPageList=True)


# find and remove titles that belong to more than one category
titles = {
    "FA": getTitles("FA.txt"),
    "FL": getTitles("FL.txt"),
    "A": getTitles("A.txt"),
    "GA": getTitles("GA.txt"),
    "B": getTitles("B.txt"),
    "C": getTitles("C.txt"),
    "Start": getTitles("Start.txt"),
    "Stub": getTitles("Stub.txt"),
}

all_titles = [title for titles in titles.values() for title in titles]
seen = set() # find duplicates https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
duplicates = set([x for x in all_titles if x in seen or seen.add(x)])

print(f"Found {len(duplicates)} titles in more than one category")

for key, value in titles.items():
    titles[key] = [title for title in value if title not in duplicates]
    writeTitles(key + ".txt", titles[key])



