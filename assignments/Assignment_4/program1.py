# PROGRAM 1

import os
import sys
import pickle

from nltk import word_tokenize
from nltk.util import ngrams

# main function that calls process_file and saves results to pickles
def main():
    
    # process English test data and write pickle
    unigrams_dict_en, bigrams_dict_en = process_file('data/LangId.train.English')
    pickle.dump(unigrams_dict_en, open('unigrams_dict_en.p', 'wb'))
    pickle.dump(bigrams_dict_en, open('bigrams_dict_en.p', 'wb'))
    
    # process French test data and write pickle
    unigrams_dict_fr, bigrams_dict_fr = process_file('data/LangId.train.French')
    pickle.dump(unigrams_dict_fr, open('unigrams_dict_fr.p', 'wb'))
    pickle.dump(bigrams_dict_fr, open('bigrams_dict_fr.p', 'wb'))
    
    # process Italian test data and write pickle
    unigrams_dict_it, bigrams_dict_it = process_file('data/LangId.train.Italian')
    pickle.dump(unigrams_dict_it, open('unigrams_dict_it.p', 'wb'))
    pickle.dump(bigrams_dict_it, open('bigrams_dict_it.p', 'wb'))
    

# read from file and generate unigram/bigram count dictionaries
def process_file(filename):
    
    current_dir = os.getcwd()  
    with open(os.path.join(current_dir, filename), 'r', encoding='utf-8') as f:
        # get text and remove newlines
        text = f.read().replace("\n", "")
    
    tokens = word_tokenize(text)
    
    # generate unigrams and bigrams
    unigrams = list(ngrams(tokens, 1))
    bigrams = list(ngrams(tokens, 2))
    
    # create dictionaries based on occurrence count
    unigram_dict = {t[0]: text.count(t[0]) for t in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
    
    return (unigram_dict, bigram_dict)

if __name__ == "__main__":
    main()
