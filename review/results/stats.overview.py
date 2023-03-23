from csvs.loader import inclusion_but_with_more as inclusion
import matplotlib.pyplot as plt
import numpy as np
import nlp.terms as terms
from latex.templating import build_template

def show_and_save(plt, file, size):
    # remove top and right spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.gcf().set_size_inches(size[0], size[1])
    plt.savefig(file, dpi=100, bbox_inches='tight', pad_inches=0.1)
    plt.show()

def year_stats():
    papers_per_year = {}
    for paper in inclusion:
        year = paper['Year']
        if year not in papers_per_year:
            papers_per_year[year] = []
        papers_per_year[year] += [paper['Id']]
    
    # sort keys
    papers_per_year = {k: papers_per_year[k] for k in sorted(papers_per_year)}

    # plot the results
    years = [int(x) for x in list(papers_per_year.keys())]
    papers = [len(papers_per_year[str(x)]) for x in years]

    plt.bar(years, papers)
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0, 20, 2))
    plt.xlabel('Year')
    plt.ylabel('# Publications')

    # add a line for the tendency
    z = np.polyfit(years, papers, 1)
    p = np.poly1d(z)
    plt.plot(years, p(years), 'r--')

    print(papers_per_year)
    show_and_save(plt, 'results/charts/years.pdf', (8, 4))

def venue_stats():
    venues = {}
    for paper in inclusion:
        venue = paper['Venue']
        id = venue['Id']
        if id == 'N/A':
            continue
        if id == 'WikiSym' or id == 'OpenSym':
            id = 'OpenSym$^1$' # OpenSym is the successor of WikiSym
            venue['Name'] = 'International Symposium on Open Collaboration'
        if id not in venues:
            venues[id] = {
                'name': venue['Name'] if venue['Type'] != 'Conference' else id + ': ' + venue['Name'],
                'type': venue['Type'],
                'papers': []
            }
        venues[id]['papers'] += [paper]

    # sort by number of papers
    venues = {k: venues[k] for k in sorted(venues, key=lambda x: len(venues[x]['papers']), reverse=True)}


    latex_content = []
    for id in venues:
        venue = venues[id]
        papers = venue['papers']
        if len(venue['papers']) > 1:
            latex_content += [venue['type'] + " & " + venue['name'].replace("&", "\\&") + " & " + str(len(papers)) + " \\\\"]

    build_template('results/latex/venues.template', 'results/latex/venues.tex', {
        'CONTENT': "\n        ".join(latex_content)
    })

    print("============= VENUE STATS (UNIQUE AUTHORS PER AUTHORS) =============")
    print("Venue #Papers UniqueAuthorsPerAuthors")
    # print formatted (Id, #papers)
    for venue in venues:
        papers = venues[venue]['papers']
        if len(papers) > 1:
            # calculate number of authors, and number of unique authors
            authors = []
            unique_authors = set()
            for paper in papers:
                for author in paper['Authors'].split(';'):
                    authors += [author]
                    unique_authors.add(author)
            print(venue, len(papers), str(round(len(unique_authors) / len(authors) * 10000) / 100) + "%")
            
def citation_stats():
    info = []
    for paper in inclusion:
        info += [{
            'year': int(paper['Year']),
            'citations': int(paper['Cits.']),
            'references': int(paper['Refs.']),
            'authors': len(paper['Authors'].split(';')),
        }]
    info = sorted(info, key=lambda x: x['year'])

    # make a scatter plot:
    # - x axis being the number of references
    # - y axis being the number of citations
    # - the size of the circle is the number of authors.
    # - make the circle transparent (alpha=0.5)
    # plot the results
    plt.scatter(
        [min(75, x['references']) for x in info], 
        [min(100, x['citations']) for x in info], 
        s=[x['authors'] * 7.5 + 10 for x in info], alpha=0.5
    )

    # log scale for the y axis
    plt.xlabel('# References')
    plt.ylabel('# Citations')
    plt.xticks(np.arange(0, 75, 10))
    plt.yticks(np.arange(0, 101, 10))
    plt.xlim(0, 75)
    plt.ylim(0, 100)

    show_and_save(plt, 'results/charts/citations.pdf', (8, 4))

    print("============= CITATION STATS =============")

    # sort paper by citations and print the top 10
    print("Top 10 papers by citations: \n(Id, Title, #Citations)")
    papers = sorted(inclusion, key=lambda x: int(x['Cits.']), reverse=True)
    for i in range(10):
        print(papers[i]['Id'], papers[i]['Title'], papers[i]['Cits.'])
    
    # do the same for the number of references
    print("\nTop 10 papers by references: \n(Id, Title, #References)")
    papers = sorted(inclusion, key=lambda x: int(x['Refs.']), reverse=True)
    for i in range(10):
        print(papers[i]['Id'], papers[i]['Title'], papers[i]['Refs.'])



def abstract_keyword_stats():
    print("============= ABSTRACT STATS =============")
    all_abstracts = [paper['Abstract'] for paper in inclusion]   
    print("Number of abstracts: ", len(all_abstracts))
    (ab_cf, ab_df) = terms.analyse_common_terms(all_abstracts)
    
    build_template('results/latex/terms.template', 'results/latex/terms.abstracts.tex', {
        'TYPE': 'Abstracts',
        'CF': '\n            '.join([
            term + ' & ' + str(ab_cf[term]) + " \\\\" for term in sorted(ab_cf, key=ab_cf.get, reverse=True)[:10]
        ]),
        'DF': '\n            '.join([
            term + ' & ' + str(ab_df[term]) + " \\\\" for term in sorted(ab_df, key=ab_df.get, reverse=True)[:10]
        ]),
    })

    print("============= KEYWORD STATS =============")
    all_keywords = [paper['Keywords'] for paper in inclusion if paper['Keywords'] != 'N/A']
    all_keywords_separated = [keyword for keywords in all_keywords for keyword in keywords.split('; ')] # flatten list
    print("Number of papers with keywords: ", len(all_keywords))
    print("Number of keywords: ", len(all_keywords_separated))
    (kw_cf, kw_df) = terms.analyse_common_terms(all_keywords) # dont pass separated bc analysis assumes a collection of documents

    build_template('results/latex/terms.template', 'results/latex/terms.keywords.tex', {
        'TYPE': 'Keywords',
        'CF': '\n            '.join([
            term + ' & ' + str(kw_cf[term]) + " \\\\" for term in sorted(kw_cf, key=kw_cf.get, reverse=True)[:10]
        ]),
        'DF': '\n            '.join([
            term + ' & ' + str(kw_df[term]) + " \\\\" for term in sorted(kw_df, key=kw_df.get, reverse=True)[:10]
        ]),
    })

venue_stats()
#citation_stats()
#abstract_keyword_stats()