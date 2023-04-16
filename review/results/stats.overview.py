from csvs.loader import inclusion_but_with_more as inclusion
import matplotlib.pyplot as plt
import numpy as np
import helpers.nlp_terms as nlpterms
import helpers.plot_saver as plotsaver
import helpers.latex_templating as latex
   

def year_stats():
    papers_per_year = {}
    for paper in inclusion:
        year = paper['Year']
        ml = paper['General']['ML']
        if year not in papers_per_year:
            papers_per_year[year] = {
                'DL': 0,
                'CL': 0,
                'Metric-based': 0,
                'Other': 0,
            }
        if 'DL' in paper['General']['ML']:
            papers_per_year[year]['DL'] += 1
        elif 'CL' in paper['General']['ML']:
            papers_per_year[year]['CL'] += 1
        elif 'metric-based' in paper['General']['Type']:
            papers_per_year[year]['Metric-based'] += 1
        else:
            papers_per_year[year]['Other'] += 1
    
    # sort keys
    papers_per_year = {k: papers_per_year[k] for k in sorted(papers_per_year)}


    # plot the results using stacked bar charts
    years = [int(x) for x in list(papers_per_year.keys())]
    
    prev = np.zeros(len(years))
    for ml in ['DL', 'CL', 'Metric-based', 'Other']:
        plt.bar(years, [papers_per_year[str(year)][ml] for year in years], bottom=prev, label=ml)
        prev = [prev[i] + papers_per_year[str(years[i])][ml] for i in range(len(years))]

    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0, 20, 2))
    plt.xlabel('Year')
    plt.ylabel('# Publications')
    plt.legend()

    plotsaver.show_and_save(plt, 'results/charts/years.pdf', (8, 4))

def venue_stats():
    venues = {}
    for paper in inclusion:
        venue = paper['Venue']
        id = venue['Id']
        if id == 'N/A':
            continue
        if id == 'WikiSym' or id == 'OpenSym':
            id = 'OpenSym$^*$' # OpenSym is the successor of WikiSym
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

    latex.build_template('results/latex/venues.template', 'results/latex/venues.tex', {
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

    # make two box plots, citations and references. use different colors for each plot 
    plt.boxplot([x['citations'] for x in info], positions=[1], widths=0.6, showfliers=False, patch_artist=True, boxprops=dict(facecolor='#1f77b4'), medianprops=dict(color='black'))
    plt.boxplot([x['references'] for x in info], positions=[2], widths=0.6, showfliers=False, patch_artist=True, boxprops=dict(facecolor='#ff7f0e'), medianprops=dict(color='black'))
    plt.xticks([1, 2], ['# Citations', '# References'])
    plt.ylabel('Count')
    plotsaver.show_and_save(plt, 'results/charts/citations.pdf', (8, 4))

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

    # TOP 15 papers by citations per year (round to two decimals)
    papers = sorted(inclusion, key=lambda x: int(x['Cits.']) / (2023 - int(x['Year'])), reverse=True)[:15]
    latex.build_template('results/latex/impactful.template', 'results/latex/impactful.tex', {
        'CONTENT': "\n        ".join([
            latex.cite_author(paper['Id'], inclusion) + " & " +
                str(round(int(paper['Cits.']) / (2023 - int(paper['Year'])), 2)) + " / " + 
                str(round(int(paper['Cits. (WOS)']) / (2023 - int(paper['Year'])), 2)) + " / " + 
                str(round(int(paper['Cits. (Scopus)']) / (2023 - int(paper['Year'])), 2)) + " / " +
            " \\\\"
        for paper in papers])
    })

def abstract_keyword_stats():
    print("============= ABSTRACT STATS =============")
    all_abstracts = [paper['Abstract'] for paper in inclusion]   
    print("Number of abstracts: ", len(all_abstracts))
    (ab_cf, ab_df) = nlpterms.analyse_common_terms(all_abstracts)
    
    latex.build_template('results/latex/terms.template', 'results/latex/terms.abstracts.tex', {
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
    (kw_cf, kw_df) = nlpterms.analyse_common_terms(all_keywords) # dont pass separated bc analysis assumes a collection of documents

    latex.build_template('results/latex/terms.template', 'results/latex/terms.keywords.tex', {
        'TYPE': 'Keywords',
        'CF': '\n            '.join([
            term + ' & ' + str(kw_cf[term]) + " \\\\" for term in sorted(kw_cf, key=kw_cf.get, reverse=True)[:10]
        ]),
        'DF': '\n            '.join([
            term + ' & ' + str(kw_df[term]) + " \\\\" for term in sorted(kw_df, key=kw_df.get, reverse=True)[:10]
        ]),
    })

def authors_stats():
    authors = {}
    for row in inclusion:
        for author in row['Authors'].split('; '):
            if author not in authors:
                authors[author] = []
            authors[author].append(row['Id'])

    # sort authors by name
    # authors = {k: v for k, v in sorted(authors.items(), key=lambda item: item[0])}
    # sort authors by number of papers then by name
    authors = {k: v for k, v in sorted(authors.items(), key=lambda item: (len(item[1]), item[0]), reverse=True)}
    # get those with more than 4 papers
    authors = {k: v for k, v in authors.items() if len(v) > 4}

    print("============= AUTHORS STATS =============")
    print("Number of authors: ", len(authors))  
    print("Number of papers: ", len(inclusion))
    print("Number of papers per author: ", len(inclusion) / len(authors))

    latex.build_template('results/latex/authors.template', 'results/latex/authors.tex', {
        'AUTHORS': '\n        '.join([
            author + ' & ' + 
            latex.cite_ids(authors[author], inclusion) + " & " +
            "(" + str(len(authors[author])) + ") \\\\"
        for author in authors]),
    })


year_stats()
venue_stats()
citation_stats()
abstract_keyword_stats()
authors_stats()

# print(latex.cite_all(inclusion))