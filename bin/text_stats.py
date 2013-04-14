#!/usr/bin/python

# Imports ###########################################################

import codecs
import nltk
import os
import os.path

from nltk.corpus import floresta


# Globals ###########################################################

TEXTS_PATH = './gutenberg/striped'


# Helpers ###########################################################

# Tagging
def simplify_tag(t):
    if "+" in t:
        return t[t.index("+")+1:]
    else:
        return t

tsents = floresta.tagged_sents()
tsents = [[(w.lower(),simplify_tag(t)) for (w,t) in sent] for sent in tsents if sent]

tagger0 = nltk.DefaultTagger('n')
tagger1 = nltk.UnigramTagger(tsents, backoff=tagger0)
tagger2 = nltk.BigramTagger(tsents, backoff=tagger1)

relevant_tags = ['v-inf', 'v-ger', 'num', 'adv', 'v-fin', 'adj', 'conj-c', 'conj-s', 'pron-det', 'v-pcp', 'n']
irrelevant_tags = ['pron-indp', 'pron-pers', 'prp', 'prop', 'art']


# Functions #########################################################

def get_cleaned_stems_list(filename):
    # Load
    raw_text = codecs.open(filename, 'r', 'latin1').read()
    token_list = nltk.word_tokenize(raw_text)

    # Tag filtering
    tagged_list = tagger2.tag(token_list)
    filtered_list = [ x[0] for x in tagged_list if x[1] in relevant_tags ]

    # Stemming
    stemmer = nltk.stem.RSLPStemmer()
    cleaned_list = [ x.replace('.', '').replace("'", "").lower() for x in filtered_list ]
    cleaned_stems_list = [ stemmer.stem(t) for t in cleaned_list if t ]

    return token_list, cleaned_stems_list


# Main ##############################################################

for filename in os.listdir(TEXTS_PATH):
    filepath = os.path.join(TEXTS_PATH, filename)
    token_list, cleaned_stems_list = get_cleaned_stems_list(filepath)
    print len(token_list), nltk.FreqDist(cleaned_stems_list).__repr__()


