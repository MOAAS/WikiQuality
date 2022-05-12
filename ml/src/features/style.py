from features.text_analysis import compute_part_of_speech

# Unimplemented features:
# - SSTPRE, SPREPW: Subordinate prepositions and conjunctions are very similar to this, so unnecessary to get an entire list of prepositions for now
# - SAV: Modal Verbs are very similar to this, so unnecessary to get an entire list of auxiliary verbs for now
# - SPV/SPVPW/SMVPPV: Difficult to detect passive voice
# - SNOMPW: Difficult to detect nominalization
# - SCHTRI/SPOSTRI: Trigrams are complex, will go back to this later

    
def compute_style_features(sentences, words, syllables, sentence_word_lengths):
    # May crash with empty or very very small texts (divisions by zero words/verbs)
    # For now, it's actually better to accept the crash, since wikipedia articles shouldn't ever have this problem, 
    #  therefore it could be an error fetching the page and it helps to detect those errors

    ft = {}

    pos_tags = compute_part_of_speech(sentences)    
    used_tags = ['PRP', 'PRP$', 'ART', 'CC', 'IN', 'WP', 'DT', 'JJ', 'NN', 'RB', 'MD', 'TB', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    articles = ['a', 'an', 'the']
    to_be = ['am', 'are', 'is', 'was', 'were', 'be', 'being', 'been']
    pos_start = {tag: 0 for tag in used_tags}  # POS counts for start of sentence
    pos_total = { tag: [] for tag in used_tags} # POS words for all sentences

    for sentence in pos_tags:
        first_word = sentence[0][0]
        first_tag = sentence[0][1]
        pos_start[first_tag] = pos_start.get(first_tag, 0) + 1

        if (first_word.lower() in articles):
            pos_start['ART'] = pos_start['ART'] + 1

        if (first_word.lower() in to_be):
            pos_start['TB'] = pos_start['TB'] + 1
        
        for [word,tag] in sentence:
            pos_total[tag] = pos_total.get(tag, []) + [word]

            if (word.lower() in articles):
                pos_total['ART'] = pos_total['ART'] + [word]
            
            if (word.lower() in to_be):
                pos_total['TB'] = pos_total['TB'] + [word]

    pos_tags = [item for sublist in pos_tags for item in sublist] # merge array of arrays
   
    ft['SSLS'] = max(sentence_word_lengths, default=0) # Largest sentence length
    ft['SSSS'] = min(sentence_word_lengths, default=0) # Shortest sentence length
    ft['SMSS'] = sum(sentence_word_lengths) / len(sentence_word_lengths) # Mean sentence length    
    ft['SLSR'] = sum([1 for length in sentence_word_lengths if length > ft['SMSS'] + 10]) / len(sentence_word_lengths) # % sentence whose size is 10 words greater than SMSS
    ft['SSSR'] = sum([1 for length in sentence_word_lengths if length < ft['SMSS'] - 5]) / len(sentence_word_lengths) # % sentence whose size is 5 words shorter than SMSS
    
    ft['SQ'] = sum([1 for sentence in sentences if sentence[-1] == '?']) # Question Count
    ft['SQPS'] = ft['SQ'] / len(sentences) # Question Count per Sentence
    ft['SE'] = sum([1 for sentence in sentences if sentence[-1] == '!']) # Exclamation Count
    ft['SEPS'] = ft['SE'] / len(sentences) # Exclamation Count per Sentence

    ft['SS'] = sum(syllables) # Syllable count

    ft['SMSPW'] = ft['SS'] / len(words) # Mean syllables per word   
    ft['SMCPW'] = sum([len(word) for word in words]) / len(words)  # Mean characters per word
    
    ft['SSTP'] = pos_start['PRP'] + pos_start['PRP$'] # Sentences starting with pronoun
    ft['SSTART'] = pos_start['ART'] # Sentences starting with article
    ft['SSTC'] = pos_start['CC'] # Sentences starting with coordinating conjunction
    ft['SSTSUB'] = pos_start['IN'] # Sentences starting with subordinating conjunction
    ft['SSTI'] = pos_start['WP'] # Sentences starting with interrogative pronoun
    ft['SSTD'] = pos_start['DT'] # Sentences starting with determiner
    ft['SSTADJ'] = pos_start['JJ'] # Sentences starting with adjective
    ft['SSTN'] = pos_start['NN'] # Sentences starting with noun
    ft['SSTADV'] = pos_start['RB'] # Sentences starting with adverb

    ft['SSTPPS'] = ft['SSTP'] / len(sentences) # Sentences starting with pronoun per sentence
    ft['SSTARTPS'] = ft['SSTART'] / len(sentences) # Sentences starting with article per sentence
    ft['SSTCPS'] = ft['SSTC'] / len(sentences) # Sentences starting with coordinating conjunction per sentence
    ft['SSTSUBPS'] = ft['SSTSUB'] / len(sentences) # Sentences starting with subordinating conjunction per sentence
    ft['SSTDPS'] = ft['SSTD'] / len(sentences) # Sentences starting with determiner per sentence
    ft['SSTADJPS'] = ft['SSTADJ'] / len(sentences) # Sentences starting with adjective per sentence
    ft['SSTNPS'] = ft['SSTN'] / len(sentences) # Sentences starting with noun per sentence
    ft['SSTADVPS'] = ft['SSTADV'] / len(sentences) # Sentences starting with adverb per sentence

    ft['SMV'] = len(pos_total['MD']) # Modal verb count
    ft['STB'] = len(pos_total['TB']) # To be verb count
    ft['SUW'] = len(set(words)) # Unique word count
    ft['SN'] = len(pos_total['NN']) # Noun count    
    ft['SUN'] = len(set(pos_total['NN'])) # Unique noun count
    verbs = pos_total['VB'] + pos_total['VBD'] + pos_total['VBG'] + pos_total['VBN'] + pos_total['VBP'] + pos_total['VBZ']
    ft['SV'] = len(verbs)
    ft['SUV'] = len(set(verbs)) # Unique verb count
    ft['SP'] = len(pos_total['PRP'] + pos_total['PRP$']) # Pronoun count
    ft['SUP'] = len(set(pos_total['PRP'] + pos_total['PRP$'])) # Unique pronoun count
    ft['SADV'] = len(pos_total['RB']) # Adverb count
    ft['SUADV'] = len(set(pos_total['RB'])) # Unique Adverb count    
    ft['SADJ'] = len(pos_total['JJ']) # Adjective count
    ft['SUADJ'] = len(set(pos_total['JJ'])) # Unique Adjective count
    ft['SCC'] = len(pos_total['CC']) # Coordinating conjunction count
    ft['SUCC'] = len(set(pos_total['CC'])) # Unique Coordinating conjunction count
    ft['SSUB'] = len(pos_total['IN']) # Subordinating conjunction count
    ft['SUSUB'] = len(set(pos_total['IN'])) # Unique Subordinating conjunction count

    ft['SMVPW'] = ft['SMV'] / len(words) # Modal verb count per word
    ft['STBPW'] = ft['STB'] / len(words) # To be verb count per word
    ft['SUWPW'] = ft['SUW'] / len(words) # Unique word count per word
    ft['SNPW'] = ft['SN'] / len(words) # Noun count per word
    ft['SUNPW'] = ft['SUN'] / len(words) # Unique noun count per word
    ft['SVPW'] = len(verbs) / len(words) # Verb count per word
    ft['SUVPW'] = len(set(verbs)) / len(words) # Unique verb count per word
    ft['SPPW'] = ft['SP'] / len(words) # Pronoun count per word
    ft['SUPPW'] = ft['SUP'] / len(words) # Unique pronoun count per word
    ft['SADVPW'] = ft['SADV'] / len(words) # Adverb count per word
    ft['SUADVPW'] = ft['SUADV'] / len(words) # Unique Adverb count per word
    ft['SADJPW'] = ft['SADJ'] / len(words) # Adjective count per word
    ft['SUADJPW'] = ft['SUADJ'] / len(words) # Unique Adjective count per word
    ft['SCCPW'] = ft['SCC'] / len(words) # Coordinating conjunction count per word
    ft['SUCCPW'] = ft['SUCC'] / len(words) # Unique Coordinating conjunction count per word
    ft['SSUBPW'] = ft['SSUB'] / len(words) # Subordinating conjunction count per word
    ft['SUSUBPW'] = ft['SUSUB'] / len(words) # Unique Subordinating conjunction count per word

    ft['STBPV'] = ft['STB'] / ft['SV'] if ft['SV'] != 0 else 0 # To be verb count per verb
    # (the check is done only here because this is virtually the only division by zero that can happen)
    
    ft['SUNPUW'] = ft['SUN'] / ft['SUW'] # Unique noun count per unique word
    ft['SUVPUW'] = ft['SUV'] / ft['SUW'] # Unique verb count per unique word
    ft['SUPPUW'] = ft['SUP'] / ft['SUW'] # Unique pronoun count per unique word
    ft['SUADJPUW'] = ft['SUADJ'] / ft['SUW'] # Unique Adjective count per unique word
    ft['SUADVPUW'] = ft['SUADV'] / ft['SUW'] # Unique Adverb count per unique word
    ft['SUCCPUW'] = ft['SUCC'] / ft['SUW'] # Unique Coordinating conjunction count per unique word
    ft['SUSUBPUW'] = ft['SUSUB'] / ft['SUW'] # Unique Subordinating conjunction count per unique word
    
    ft['SWL6'] = len([w for w in words if len(w) > 6]) # words larger than 6 letters

    return ft
