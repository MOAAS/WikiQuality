
def build_template(template, dest, replacements):
    with open(template, 'r') as ffrom, open(dest, 'w', encoding='utf-8') as fto:
        strn = ffrom.read()
        for key in replacements:
            strn = strn.replace('{{' + key + '}}', str(replacements[key]))
        fto.write(strn)
    return strn

def cite_ids(ids, inclusion):
    ids = [str(x) for x in ids]
    papers = [p for p in inclusion if str(p['Id']) in ids]
    return '\\cite{' + ', '.join([p['Bibtex'] for p in papers]) + '}'

def cite_author(id, inclusion):
    paper = [p for p in inclusion if str(p['Id']) == str(id)][0]
    cite_part = '~\\cite{' + paper['Bibtex'] + '}'

    # IF only one author, use last name. if two authors, use first and last name. if more than two, use first name and et al.
    all_authors = paper['Authors'].split('; ')
    if len(all_authors) == 1:
        author_part = all_authors[0].split(' ')[-1]
    elif len(all_authors) == 2:
        author_part = all_authors[0].split(' ')[-1] + " and " + all_authors[1].split(' ')[-1]
    else:
        author_part = all_authors[0].split(' ')[0] + " et al."
    return author_part + cite_part
