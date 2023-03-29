
def build_template(template, dest, replacements):
    with open(template, 'r') as ffrom, open(dest, 'w') as fto:
        str = ffrom.read()
        for key in replacements:
            str = str.replace('{{' + key + '}}', replacements[key])
        fto.write(str)
    return str

def cite_ids(ids, inclusion):
    ids = [str(x) for x in ids]
    papers = [p for p in inclusion if str(p['Id']) in ids]
    return ', '.join(['\\cite{' + p['Bibtex'] + '}' for p in papers])
