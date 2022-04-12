import re
import nltk
from regex import W
import syllables
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# For help with the NLTK POS tagging, see:
# https://www.nltk.org/book/ch05.html
# https://www.nltk.org/api/nltk.tag.html
# Run in python: nltk.help.upenn_tagset('<TAG>') to see what the tags mean
# This url contains a list of most tags: https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk 

def compute_words(string):
    words = nltk.word_tokenize(string)


    # keep any word that contains a letter or digit
    words = [word for word in words if re.search(r'[\w]', word)]    

    if (len(words) <= 1):
        return words

    # For every word that is "'s", concatenate it to the end of the previous word
    words = [words[i] + words[i+1] if words[i + 1] == "'s" else words[i] for i in range(len(words)-1)] + [words[-1]]

    # Remove all words that are 's
    words = [word for word in words if word != "'s"]    

    return words

def compute_sentences(plaintext):
    # remove all lines that start with == and end with ==    
    withoutHeaders = re.sub(r'^==.*==$', '', plaintext, flags=re.MULTILINE)

    return nltk.sent_tokenize(withoutHeaders)

def estimate_syllables(word):
    return syllables.estimate(word)

def compute_part_of_speech(sentences):
    return nltk.tag.pos_tag_sents([nltk.word_tokenize(sentence) for sentence in sentences], lang='eng')