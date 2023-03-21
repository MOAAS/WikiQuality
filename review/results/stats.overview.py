from csvs.loader import inclusion_but_with_more as inclusion
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

    with open('results/latex/venues.tex', 'w') as f:
        f.write("\\begin{table}[htbp]\n")
        f.write("    \\caption{Overview of the venues}\n")
        f.write("    \\label{tab:venues}\n")
        f.write("    \\centering\n")
        f.write("    \\begin{tabular}{c m{0.65\\textwidth} c}\n")
        f.write("        \\toprule\n")
        f.write("        \\textbf{Type} & \\textbf{Venue} & \\textbf{\# Papers} \\\\\n")
        f.write("        \\midrule\n")

        # add all venues with more than 1 paper
        for id in venues:
            venue = venues[id]
            papers = venue['papers']
            if len(venue['papers']) > 1:
                # papers_cite = "\\cite{" + ", ".join([papers[i]['Bibtex'] for i in range(len(venue['papers']))]) + "}"

                f.write("        " + 
                    venue['type'] + " & " + 
                    venue['name'].replace("&", "\\&") + " & " + 
                    str(len(papers)) + " \\\\\n"
                )
        
        f.write("        \\bottomrule\n")
        f.write("    \\end{tabular}\n")
        f.write("    \\\\ \\vspace{0.1cm}\n")
        f.write("    \\footnotesize\n")
        f.write("    $^1$ Formerly WikiSym\n")
        f.write("\\end{table}\n")


    # for venue in venues:
    #     print(venue, venues[venue]['type'], venues[venue]['name'], len(venues[venue]['papers']))
        
venue_stats()