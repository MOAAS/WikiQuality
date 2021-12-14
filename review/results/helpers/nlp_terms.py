import string
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))
stop_words.add('the')
stop_words.add('we')
stop_words.add('based')

def singularize(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)
    
def normalize_string(str):
    # remove punctuation, lowercase, remove stopwords

    str = str.lower()
    word_tokens = word_tokenize(str)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = [w for w in filtered_sentence if not w in string.punctuation]
    filtered_sentence = [singularize(w) for w in filtered_sentence]

    return filtered_sentence

def calculate_document_frequencies(documents):
    # the total number of documents in which the term t occurs
    dfs = {}
    for document in documents:
        visited = set()
        filtered_sentence = normalize_string(document)
        for word in filtered_sentence:
            if word in visited:
                continue
            visited.add(word)
            if word in dfs:
                dfs[word] += 1
            else:
                dfs[word] = 1     

    return dfs        

def calculate_collection_frequencies(collection):
    # the total number of times the term t occurs in the collection (string)
    cfs = {}
    filtered_sentence = normalize_string(collection)
    for word in filtered_sentence:
        if word in cfs:
            cfs[word] += 1
        else:
            cfs[word] = 1

    return cfs


def analyse_common_terms(documents):
    collection = "\n".join(documents)
    dfs = calculate_document_frequencies(documents)
    cfs = calculate_collection_frequencies(collection)

    print("Number of words: ", len(collection.split()))
    return cfs, dfs
