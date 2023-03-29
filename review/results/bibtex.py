from csvs.loader import inclusion_but_with_more as inclusion
import urllib.parse

bibtexes = []
for paper in inclusion:
    venue = paper['Venue']
    venue_type = venue['Type']

    bibtex = {}
    bibtex['name'] = paper['Bibtex']
    bibtex['author'] = paper['Authors'].replace(';', ' and ')
    bibtex['year'] = paper['Year']
    bibtex['title'] = paper['Title']
    bibtex['url'] = paper['URL']
    bibtex['url'] = urllib.parse.quote(bibtex['url'], safe=':/?=') # escape special characters


    if (venue_type == "Conference"):
        bibtex['type'] = "inproceedings"
        bibtex['booktitle'] = venue['Venue']

        # if 'pp.' in pub_venue:
        #     bibtex['pages'] = pub_venue.split('pp.')[1].strip()
    elif (venue_type == "Journal"):
        bibtex['type'] = "article"
        bibtex['journal'] = venue['Venue']

        if 'Volume' in venue:
            bibtex['volume'] = venue['Volume']
            if 'Issue' in venue:
                bibtex['issue'] = venue['Issue']
        
        if 'Pages' in venue:
            bibtex['pages'] = venue['Pages']
    elif (venue_type == "Book"):
        bibtex['type'] = "book"
        bibtex['journal'] = venue['Venue']
    elif (venue_type == "Other"):
        bibtex['type'] = "misc" 
        bibtex['journal'] = venue['Venue']
    else:
        bibtex['type'] = "misc"

    bibtexes += [bibtex]

full_str = ""
for bibtex in bibtexes:
    full_str += "@" + bibtex['type'] + "{" + bibtex['name'] + ",\n"
    for key in [x for x in bibtex.keys() if x != 'name' and x != 'type']:
        full_str += "    " + key + " = {" + bibtex[key].replace('&', '\&').replace('%', '\%') + "},\n"
    full_str += "}"
    full_str += "\n\n"
full_str = full_str.strip()


def save_string_to_file(f, str):
    f.write(str)
    f.write("\n")

# save to file
with open('results/latex/bibtex.bib', 'w', encoding='UTF-8') as f:
    f.write(full_str)
    f.close()
