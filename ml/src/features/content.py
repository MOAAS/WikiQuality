import re
from wikitext_cleaner import remove_html_tag, remove_br
from statistics import stdev

# Unimplemented features:
# - CIBL: Internal Broken Link Count (doable by getting list of all titles in wiki and checking if they exist)

# New features
# - CTB: Number of tables
# - CUCT: Number of unique templates

SECTION_REGEX = r'\n==([^=]*)==\n'
SUBSECTION_REGEX = r'\n===([^=]*)===\n'
SUBSUBSECTION_REGEX = r'\n====([^=]*)====\n'

def compute_sections(plaintext):
    sections = re.split(SECTION_REGEX, plaintext) # find all sections in string


    sectionsDict = {}
    sectionsDict['Intro'] = sections[0]
    sectionTitles = sections[1::2]
    sections = sections[2::2]
            
    for i in range(len(sections)):
        sectionsDict[sectionTitles[i].strip()] = sections[i]
    
    # remove dictionary items with length 0
    sectionsDict = {k: v for k, v in sectionsDict.items() if len(v) > 0}



    return sectionsDict

def compute_content_features(wikitext, plaintext, words, sentences):
    sections = compute_sections(plaintext)
    section_lengths = [len(sections[section]) for section in sections]     
    norefs_text = remove_html_tag(remove_br(wikitext), 'ref')

    ft = {}

    # Content Features
    ft['CC'] = len(plaintext) # Character Count
    ft['CW'] = len(words) # Word Count 
    ft['CSN'] = len(sentences) # Sentence Count 
    ft['CS'] = max(1, len(sections)) # Section Count (minimum of 1: edge case)
    ft['CMSL'] = sum(section_lengths) / ft['CS'] # Mean Section Length (Characters)   
    ft['CP'] = len(re.findall(r'\n\n', plaintext)) + 1 # Paragraph Count
    ft['CMPL'] = ft['CC'] / ft['CP'] # Mean Paragraph Length   
    ft['CLSL'] = max(section_lengths, default=0) # Largest section length
    ft['CSSL'] = min(section_lengths, default=0) # Shortest section length
    ft['CSTDSL'] = 0 if len(section_lengths) <= 1 else stdev(section_lengths) # Standard Deviation of Section Length
    ft['CLSSR'] =  ft['CLSL'] / ft['CSSL'] # Longest-Shortest Section Ratio
    ft['CB'] = len(re.findall(SUBSECTION_REGEX, wikitext)) # Subsection Count
    ft['CBPS'] = ft['CB'] / ft['CS'] # Subsection Count per Section
    ft['CNL'] = len(sections['Intro']) # Introduction Length (Characters)
    ft['CNLTLR'] = ft['CNL'] / ft['CC'] # Introduction Length-Text Length Ratio    
    ft['CR'] =  len(re.findall(r'<ref[^/]*>', wikitext)) # Reference Count (number of <ref> tags that don't self close) (possibly missing: 'refn', 'efn', 'sfn|', 'r|')
    ft['CCC'] = len(re.findall(r'<ref', wikitext))  # Citation Count (same as above but self-closing counts)
    ft['CCCPC'] = ft['CCC'] / ft['CC'] # Citation Count per Character
    ft['CCCPS'] = ft['CCC'] / ft['CS'] # Citation Count per Section
    ft['CEL'] = len(re.findall(r'\[http(.*?)\]', norefs_text)) # External Link Count (find [<url>...] but outside ref tags)
    ft['CELPS'] = ft['CEL'] / ft['CS'] # External Link Count per Section
    ft['CELPC'] = ft['CEL'] / ft['CC'] # External Link Count per Character

    # Internal Link Count (find [[<title>]] but outside ref tags), filter all internal links starting with File:, Category: or Image:
    ft['CIL'] = len([link for link in re.findall(r'\[\[(.*?)\]\]', norefs_text) if not link.startswith(('File:', 'Category:', 'Image:'))])
    ft['CILPC'] = ft['CIL'] / ft['CC'] # Internal Link Count per Character    

    
    base_images = len(re.findall(r'\[\[(Image:|File:)(.*?)\]\]', wikitext))
    galleries = re.findall(r'<gallery[^>]*>(.*?)</gallery>', wikitext, flags=re.DOTALL | re.IGNORECASE)
    gallery_images = sum([len(re.findall(r'File:', gallery)) for gallery in galleries])
    
    ft['CI'] = base_images + gallery_images # Image Count

    ft['CIPC'] = ft['CI'] / ft['CC'] # Image Count per Character
    ft['CIPS'] = ft['CI'] / ft['CS'] # Image Count per Section
    ft['CL3'] = len(re.findall(SUBSUBSECTION_REGEX, wikitext)) # Number of L3 headings 
    ft['CIB'] = len(re.findall(r'{{Infobox', wikitext, flags=re.IGNORECASE)) # Number of Information Boxes
    ft['CCT'] = len(re.findall(r'{{Cit', wikitext, flags=re.IGNORECASE)) # Number of citation templates
    ft['CNCT'] = len(re.findall(r'{{', wikitext)) - ft['CCT'] # Number of non-citation templates

    # New features
    ft['CTB'] = len(re.findall(r'\{\|', wikitext, flags=re.IGNORECASE)) # Number of tables
    ft['CUCT'] = len(set([template.strip() for template in re.findall(r'{{(.*?)[|\n}]', wikitext, flags=re.DOTALL | re.IGNORECASE)])) # Unique template count

    return ft
