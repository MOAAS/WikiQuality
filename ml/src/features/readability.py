import math
import os

READABILITY_FEATURES = ['RARI', 'RCL', 'RFRE', 'RFK', 'RGFI', 'RLBI', 'RSG', 'RDWS', 'RDC', 'RLWF']

# easy words must also take into account:
# - verb conjugation (if not irregular), 
# - plural of nouns
# - possessive ('s)
# - Familiar names (e.g. some Countries and Surnames)
with open(os.path.join(os.path.dirname(__file__), 'EasyWordList.txt'), 'r', encoding='utf-8') as f:
    EASY_WORDS = [word.lower() for word in f.read().split('\n')]



def compute_readability_features(sentences, words, syllables):

    ft = {}

    num_syllables = sum(syllables)
    num_sentences = len(sentences)
    num_words = len(words)
    num_characters = sum(len(word) for word in words)

    num_polysyllables = sum([1 for syllable in syllables if syllable > 2])
    num_large_words = sum([1 for word in words if len(word) > 6])

    num_difficult_words = sum([1 for word in words if word not in EASY_WORDS])

    ft['RARI'] = 4.71 * num_characters / num_words + 0.5 * num_words / num_sentences - 21.43 # Automated Readability Index
    ft['RCL'] = 5.88 * num_characters / num_words - 29.6 * num_sentences / num_words - 15.8 # Coleman-Liau Index
    ft['RFRE'] = 206.835 - 1.015 * num_words / num_sentences - 84.6 * num_syllables / num_words # Flesch-Reading ease
    ft['RFK'] = 0.39 * num_words / num_sentences + 11.8 * num_syllables / num_words - 15.59 # Flesch-Kincaid Index
    ft['RGFI'] = 0.4 * (num_words / num_sentences + 100 * num_polysyllables / num_words) # Gunning-Fog Index
    ft['RLBI'] = num_words / num_sentences + 100 * num_large_words / num_words # Lasbarhets Index
    ft['RSG'] = 1.043 * math.sqrt(num_polysyllables * 30 / num_sentences) + 3.1291 # SMOG Index

    ft['RDWS'] = num_difficult_words # Difficult Word Score
    ft['RDC'] = 0.1579 * (100 * num_difficult_words / num_words ) + 0.0496 * num_words / num_sentences # Dale-Chall Index

    n1 = num_words - num_polysyllables
    n2 = num_polysyllables
    n3 = (n1 + 3 * n2) / (num_sentences)
    ft['RLWF'] = n3 / 2 if n3 > 20 else n3 / 2 - 1 # Linsear Write Formula

    return ft
