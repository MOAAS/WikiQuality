from csvs.loader import inclusion

import matplotlib.pyplot as plt
import numpy as np

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
    show_and_save(plt, 'charts/years.pdf', (8, 4))

def venue_stats():
    venues = {}
        
venue_stats()