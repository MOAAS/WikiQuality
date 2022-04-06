import re
import datetime
import unittest

RE_FLAGS_CI = re.DOTALL | re.IGNORECASE # Dotall matches . to newlines too

def write_file(filename, string):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(string)

def read_file(filename):
    with open(filename, 'r', encoding='utf8') as f:
        return f.read()

def remove_pattern(string, starting_pattern, ending_pattern):
    # escape patterns for regex
    starting_pattern = re.escape(starting_pattern)
    ending_pattern = re.escape(ending_pattern)


    # compile regex with ignorecase and dotall

    pattern = re.compile(starting_pattern + r'.*?' + ending_pattern, flags=RE_FLAGS_CI)

    # return filtered
    return re.sub(pattern, '', string)

def keep_whats_inside(string, starting_pattern, ending_pattern):
    # escape patterns for regex
    starting_pattern = re.escape(starting_pattern)
    ending_pattern = re.escape(ending_pattern)

    # compile regex
    pattern = re.compile(starting_pattern + r'(.*?)' + ending_pattern, flags=RE_FLAGS_CI)

    return re.sub(pattern, r'\1', string)

def remove_html_tag(string, tag):
    # need all these whitespaces because sometimes there are extra spaces between tags and <>'s
    pattern = re.compile(r'<\s*' + tag + r'\s*(.*?)(</?\s*' + tag + r'\s*>|\s*/>)', flags=RE_FLAGS_CI)

    return re.sub(pattern, '', string) 

def remove_br(string):    
    string = re.sub(r'<\s*br\s*>', '', string, flags=RE_FLAGS_CI)
    string = remove_html_tag(string, 'br')
    return string

def remove_pattern_with_matching_brackets(string, starting_pattern, bracket_open, bracket_close, num_starting_brackets):  
    # find every index of starting pattern
    starting_indices = [m.start() for m in re.finditer(re.escape(starting_pattern), string, flags=RE_FLAGS_CI)]
    starting_indices.reverse() # run reversed so we can edit string in place

    for start_index in starting_indices:
        # find index of end of pattern
        end_index = start_index + num_starting_brackets
        numBrackets = num_starting_brackets

        has_failed = False
        while numBrackets > 0:
            # if end string
            if end_index == len(string) - 1:
                #print(starting_pattern + " " + bracket_open + " " + bracket_close + " " + " " + str(num_starting_brackets) + " " + str(starting_indices))
                #print(string[start_index:start_index+3000])

                if (starting_pattern == '{|'): # dumb edge case, sometimes they forget to close the tables (hope it's the only one)          
                    print("We're missing a closing |} somewhere, but it's ok... We're going to try and find that :P")
                    end_index = string.find('\n\n', start_index)  # find empty line from start_index
                else:
                    print("Warning... Did not find end of pattern with matching brackets...\n")
                    has_failed = True
                break
            
            end_index += 1
            if string[end_index] == bracket_open:
                numBrackets += 1
            elif string[end_index] == bracket_close:
                numBrackets -= 1    

        if has_failed:
            continue
        # remove pattern
        string = string[:start_index] + string[end_index+1:]  

    return string
    
def clean_math(string, starting_pattern, ending_pattern):
    starting_pattern = re.escape(starting_pattern)
    ending_pattern = re.escape(ending_pattern)
    pattern = re.compile(starting_pattern + r'(.*?)' + ending_pattern, flags=RE_FLAGS_CI)
    
    # (todo: instead replace fracs, logs, sqrts and lims? idk)
    def replaceMath(match):
        str = match.group(0)

        # if match contains \
        if '\\' in str:
            return ''
        elif '<math' in str:
            str = match.group(0).split('|')[-1]
            # return everything after '>' and before '</math>
            return str[str.find('>')+1:str.rfind('</math>')]
        else:
            return match.group(1).split('|')[-1]

    return re.sub(pattern, replaceMath, string)

def clean_wikitext(wikitext, title, writeToFile=False):
    savedWikiText = wikitext

    ### Remove final sections (references and notes), if there are any
    final_sections = ["References", "Notes", "Notes and references", "External Links", "See also"]
    for section in final_sections:
        wikitext = wikitext.split('==' + section + '==')[0]
        wikitext = wikitext.split('== ' + section + ' ==')[0]

    ### General initial tweaks
    wikitext = re.sub(r'&nbsp;', ' ', wikitext) # replace &nbsp; with space    
    wikitext = re.sub(r'{{nbsp}}', ' ', wikitext) # replace {{nbsp}} with space        
    wikitext = re.sub(r'&thinsp;', ' ', wikitext) # replace &thinsp; with space    
    wikitext = re.sub(r'&minus;', '-', wikitext) # replace &minus; with -    
    wikitext = re.sub(r'{{CURRENTYEAR}}', str(datetime.datetime.now().year), wikitext, flags=re.IGNORECASE) ## replace {{currentyear}} with current year

    
    ### Remove html tags (Usually buggy and sometimes don't respect nesting rules)
    wikitext = remove_br(wikitext) # remove all instances of <br>, before removing other tags, sometimes they dont close
    wikitext = remove_pattern(wikitext, '<!--', '-->')
    wikitext = keep_whats_inside(wikitext, '<p>', '</p>')
    html_tags = ['ref', 'span', 'div', 'section', 'noinclude', 'onlyinclude', 'timeline', 'gallery']


    for tag in html_tags:
        wikitext = remove_html_tag(wikitext, tag)    

    ### Remove stuff with squared brackets
    wikitext = remove_pattern_with_matching_brackets(wikitext, '[[File:', '[', ']', 2)
    wikitext = remove_pattern_with_matching_brackets(wikitext, '[[Category:', '[', ']', 2)
    wikitext = remove_pattern_with_matching_brackets(wikitext, '[[Image:', '[', ']', 2)

    def replaceSingleSquareBracket(match):
        str = match.group(1)
        # if match starts with http
        if str.startswith('http'):
            # if has space, split on first space only, else return empty string
            if ' ' in str:
                return str.split(' ', 1)[-1]
            else:
                return ''
        else:
            return match.group(0)
    def replaceDoubleSquareBracket(match):
        str = match.group(1)
        # if match contains '|' return what's after '|', else return everything except brackets
        if '|' in str:
            return str.split('|', 1)[1]
        else:            
            return str

    wikitext = re.sub(r'\[\[(.*?)\]\]', replaceDoubleSquareBracket, wikitext)
    wikitext = re.sub(r'\[(.*?)\]', replaceSingleSquareBracket, wikitext)
    
    ### Remove initial tags
    initial_blocks = [
        'Other uses', 'displaytitle', 'Short description|', 'About|', 'Use', 'bots|', 'Engvar', 'Dabnav',
        'pp-', 'pp|', 'hatnote', 'for|', 'italic title', 'good article', 'featured article', 'TOC',
        'subcat', 'nutshell', 'guideline', 'Linking and page manipulation', 'polluted category'
    ]
    for block in initial_blocks:
        wikitext = remove_pattern(wikitext, '{{' + block, '}}')
    wikitext = remove_pattern(wikitext, '__FORCETOC__', '')
    wikitext = remove_pattern(wikitext, '__TOC__', '')

    ### Remove specific tags
    curly_bracket_blocks = [
        'IPA', 'Clarify', 'Redirect', 'glossary', 'wikipedia glossary', 'quote box', 'portal', 'see also|', 'see|', 'main|', 'update|', 
        'shortcut', 'expand section|', 'citation needed|', 'more citations needed|', 'additional citation needed|', 'refimprove|', 
        'self reference|', 'updated|', 'details|', 'update',
        'clear', 'anchor', 'colbegin', 'colend', 'col-', 'col ', 'div col', 'div col', 
        'certification table', 'stack', 'notelist', 'note|', 'dynamic list', 'wikt|', 'reflist', 'unsolved', 'surname', 'campaignbox',
        'further|', 'distinguish', 'chembox',  'mycomorphbox', 'speciesbox', 'automatic taxobox', 'clade', 'cladogram', 'block indent', 
        'multiple image', 'listen', 'infobox', 'wide image', 'graph', 'location map', 'rapid transit', 'external media', 'bar chart',
        'chess diagram', 'album ratings', 'track listing', 'aired episodes', 'episode', 'television', 'video game timeline', 'gallery',
        'Formatprice', 'inflation', 'markup', 'cmbox', 'POV section', 'CSS', 'quotebox', 'Football', 'fs ','fb ',
        'rp', 'pn', 'refn', 'efn', 'sfn|', 'r|', 'cn', 'refimprove', 
    ]



    for block in curly_bracket_blocks:
        wikitext = remove_pattern_with_matching_brackets(wikitext, '{{' + block, '{', '}', 2)
    wikitext = remove_pattern_with_matching_brackets(wikitext, '{|', '{', '}', 1) # removing tags like: {| class="wikitable"...

 

    ### Formatting tags
    wikitext = re.sub(r'{{wikt-lang\|(.*?)\|(.*?)}}', r'\2', wikitext, flags=RE_FLAGS_CI) # replace {{wikt-lang|x|y}} with y        
    wikitext = re.sub(r'{{lang-(.*?)\|(.*?)}}', lambda m : m.group(2).split('|')[0], wikitext, flags=RE_FLAGS_CI) # replace {{lang-*|x}} with x        
    wikitext = re.sub(r'{{lang\|(.*?)\|(.*?)}}', r'\2', wikitext, flags=RE_FLAGS_CI) # replace {{lang|x|y}} with y        
    wikitext = re.sub(r'{{mvar\|(.*?)}}', r'\1', wikitext, flags=RE_FLAGS_CI) # replace {{mvar|x}} with x
    wikitext = re.sub(r'{{wiktla\|(.*?)}}', r'\1', wikitext, flags=RE_FLAGS_CI) # replace {{wiktla|x}} with x
    wikitext = re.sub(r'{{circa}}', r'c.', wikitext, flags=RE_FLAGS_CI) # replace {{circa}} with c.
    wikitext = re.sub(r'{{circa\|(.*?)}}', lambda m : 'c. ' + m.group(1).split('|')[-1], wikitext, flags=RE_FLAGS_CI) # replace {{circa|x|..|y} with c. y
    wikitext = re.sub(r'{{(convert|cvt)\|(.*?)\|(.*?)}}', lambda m : m.group(2) + ' ' + m.group(3).split('|')[0], wikitext, flags=RE_FLAGS_CI) # replace {{convert|x|y|z}} with x y    
    wikitext = re.sub(r'{{ndash}}', '-', wikitext, flags=RE_FLAGS_CI) # replace {{ndash}} with -
    wikitext = re.sub(r'{{coord\|(.*?)\|(.*?)\|(.*?)}}', r'\1' + '°N ' + r'\2' + '°E', wikitext, flags=RE_FLAGS_CI) # replace {{Coord|x|y|z}} with x°N, y°W
    
    wikitext = keep_whats_inside(wikitext, "'''", "'''")
    wikitext = keep_whats_inside(wikitext, "''", "''")
    wikitext = keep_whats_inside(wikitext, '=====', '=====')
    wikitext = keep_whats_inside(wikitext, '====', '====')
    wikitext = keep_whats_inside(wikitext, '===', '===') 
    # wikitext = keep_whats_inside(wikitext, '==', '==') # keep section headers in, doesn't hurt a lot and helps extracting sections

    wikitext = keep_whats_inside(wikitext, '<sub>', '</sub>')
    wikitext = keep_whats_inside(wikitext, '<sup>', '</sup>')
    wikitext = keep_whats_inside(wikitext, '<small>', '</small>')
    wikitext = keep_whats_inside(wikitext, '<strong>', '</strong>')
    wikitext = keep_whats_inside(wikitext, '{{small|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{strong|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{#expr:', '}}')
    # todo: do keep_whats_inside for html tags. e.g. <poem>, <syntaxhighlight>, <code>, etc.
    wikitext = keep_whats_inside(wikitext, '<code>', '</code>')
    wikitext = keep_whats_inside(wikitext, '<nowiki>', '</nowiki>')
    wikitext = keep_whats_inside(wikitext, '<syntaxhighlight', '</syntaxhighlight>')
    wikitext = keep_whats_inside(wikitext, '<blockquote>', '</blockquote>')
    wikitext = keep_whats_inside(wikitext, '<center>', '</center>')
    wikitext = keep_whats_inside(wikitext, '{{Blockquote\n|text=', '}}')    
    wikitext = keep_whats_inside(wikitext, '{{Blockquote|text=', '}}')    
    wikitext = keep_whats_inside(wikitext, '{{block quote', '}}')    
    wikitext = keep_whats_inside(wikitext, '{{blockquote|', '}}')    
    wikitext = keep_whats_inside(wikitext, '{{cquote|', '}}')   
    wikitext = keep_whats_inside(wikitext, '{{quote|text=', '}}')   
    wikitext = keep_whats_inside(wikitext, '{{quote|', '}}')   
    wikitext = keep_whats_inside(wikitext, '{{poemquote|', '}}')   
    wikitext = keep_whats_inside(wikitext, '{{center|', '}}')   
    wikitext = keep_whats_inside(wikitext, '{{gaps', '}}')
    wikitext = keep_whats_inside(wikitext, '{{sic|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{section link|', '}}')
    wikitext = remove_pattern(wikitext, '{{legend', '}}')
    wikitext = remove_pattern(wikitext, '{{tl|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{tlx|', '}}')
   

    # Remove/Clean Math tags (todo: instead replace fracs, logs, sqrts and lims? idk)
    wikitext = re.sub(r'{{=}}', '=', wikitext) # replace {{=}} with =
    wikitext = re.sub(r'{{pi}}', 'π', wikitext) # replace {{pi}} with π    
    wikitext = re.sub(r'{{sfrac\|(.*?)\|(.*?)}}', r'\1/\2', wikitext) # replace {{sfrac|x|y}} with x/y
    wikitext = keep_whats_inside(wikitext, '{{isup|', '}}')

    wikitext = clean_math(wikitext, ':<math', '</math>')
    wikitext = clean_math(wikitext, '<math', '</math>')
    wikitext = clean_math(wikitext, '{{math|1=', '}}')
    wikitext = clean_math(wikitext, '{{math', '}}')
    wikitext = clean_math(wikitext, '{{tmath', '}}')
    wikitext = clean_math(wikitext, '{{nowrap|1=', '}}')
    wikitext = clean_math(wikitext, '{{nowrap', '}}')

    ### Other stuff
    wikitext = keep_whats_inside(wikitext, '{{chessgloss|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{defn|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{term|', '}}')
    wikitext = keep_whats_inside(wikitext, '{{ordered list|lost_style_type=lower-roman', '}}')
    wikitext = keep_whats_inside(wikitext, '{{ordered list', '}}')

    ### Final tweaks
    wikitext = re.sub(r'\|', ' ', wikitext)
    wikitext = keep_whats_inside(wikitext, '{{', '}}')

    wikitext = wikitext.strip() # trim 
    wikitext = re.sub(r'\n\n\n+', '\n\n', wikitext) # convert multiple empty lines to one
    
    if writeToFile:
        # escape title for filename
        title = re.sub(r'[^\w\s]', '', title)
        write_file('test/wikitext-' + title + '.txt', savedWikiText)
        write_file('test/wikitextclean-' + title + '.txt', wikitext)

    return wikitext

class TestFeatures(unittest.TestCase):
    # constructor
    def setUp(self):
        self.maxDiff = None
    
    def test_wikiclean(self):
        titles = [
            "Gel", "SP 500", "Nicolas Cage", "En passant", "2022 Russian invasion of Ukraine", "Car", 
            "Bluetooth", "History of Wine", "Cars 2", "Despacito", "List of The Expanse episodes",
            "List of mostliked YouTube videos", "7 World Trade Center", "Crescent honeyeater",
            "E mathematical constant", "Eulers constant", "Archimedes", "Quantum computing",
            "Crucifixion and Last Judgement diptych", "Thalassodromeus", "Cladogram", "Glucose",
            "Gas chromatography", "Grip tennis", "Psilocybe semilanceata", "Abbreviation",
            "1860 Boden Professor of Sanskrit election", "Among Us", "Renewable energy in Scotland",
            "Exit Speed", "New Rochelle 250th Anniversary half dollar", "Cretoxyrhina", "Ancient Greek",
            "London Necropolis Company", "Cyclol", "WikipediaExternal links", 'Frits Palm', 'Kolkata Metro',
        ]
        for title in titles:
            with open('ml/test/wikitext-' + title + '.txt', 'r', encoding='utf8') as f:
                wikitext = f.read()
            
            result = clean_wikitext(wikitext, title, writeToFile=False)

            with open('ml/test/wikitextclean-' + title + '.txt', 'r', encoding='utf8') as f:
                wikitext_clean = f.read()


            if (result != wikitext_clean):
                with open('ml/test/FAIL-wikitext-clean.txt', 'w', encoding='utf8') as f:
                    f.write("FAIL REPORT: " + title + "\n")
                    f.write(result)

                with open('ml/test/CORRECT-wikitext-clean.txt', 'w', encoding='utf8') as f:
                    f.write("CORRECT REPORT: " + title + "\n")
                    f.write(wikitext_clean)

                self.assertEqual(wikitext_clean, result)

if __name__ == '__main__':
    unittest.main()