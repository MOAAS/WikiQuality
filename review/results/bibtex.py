from csvs.loader import inclusion
import urllib.parse

bibtexes = []
for paper in inclusion:
    pub_type = paper['Publication Type']
    pub_venue = paper['Published In']

    bibtex = {}
    bibtex['name'] = paper['Authors'].split(';')[0].split(' ')[-1] + paper['Year'] + "_lr" + paper['Id']
    bibtex['author'] = paper['Authors'].replace(';', ' and ')
    bibtex['year'] = paper['Year']
    bibtex['title'] = paper['Title']
    bibtex['url'] = paper['URL']
    bibtex['url'] = urllib.parse.quote(bibtex['url'], safe=':/?=&') # escape special characters


    if (pub_type == "Conference"):
        bibtex['type'] = "inproceedings"
        bibtex['booktitle'] = pub_venue.split(',')[0]

        # if 'pp.' in pub_venue:
        #     bibtex['pages'] = pub_venue.split('pp.')[1].strip()
    elif (pub_type == "Journal"):
        bibtex['type'] = "article"

        bibtex['journal'] = pub_venue.split(',')[0]

        if 'vol.' in pub_venue:
            volume_part = pub_venue.split('vol.')[1].split(',')[0]
            bibtex['volume'] = volume_part.split('(')[0].strip()
            if '(' in volume_part:
                bibtex['issue'] = volume_part.split('(')[1].split(')')[0].strip()
            
        if 'pp.' in pub_venue:
            bibtex['pages'] = pub_venue.split('pp.')[1].strip()
    else:
        bibtex['type'] = "misc"

    bibtexes += [bibtex]

full_str = ""
for bibtex in bibtexes:
    full_str += "@" + bibtex['type'] + "{" + bibtex['name'] + ",\n"
    for key in [x for x in bibtex.keys() if x != 'name' and x != 'type']:
        full_str += "    " + key + " = {" + bibtex[key] + "},\n"
    full_str += "}"
    full_str += "\n\n"
full_str = full_str.strip()


def save_string_to_file(f, str):
    f.write(str)
    f.write("\n")

# save to file
with open('results/bibtex.bib', 'w', encoding='UTF-8') as f:
    f.write(full_str)
    f.close()
