# PROGRAM 2

import pickle
import os

from nltk import word_tokenize
from nltk.util import ngrams

# read dictionaries from pickle files, calculate probability of each language based on test file,
# and write output to output.txt
def main():
    
    unigrams_dict_en = pickle.load(open('unigrams_dict_en.p', 'rb'))  
    bigrams_dict_en = pickle.load(open('bigrams_dict_en.p', 'rb'))  
        
    unigrams_dict_fr = pickle.load(open('unigrams_dict_fr.p', 'rb'))  
    bigrams_dict_fr = pickle.load(open('bigrams_dict_fr.p', 'rb'))  
    
    unigrams_dict_it = pickle.load(open('unigrams_dict_it.p', 'rb'))  
    bigrams_dict_it = pickle.load(open('bigrams_dict_it.p', 'rb'))  
    
    total_vocab_cnt = len(unigrams_dict_en) + len(unigrams_dict_fr) + len(unigrams_dict_it)
    
    current_dir = os.getcwd()
    with open(os.path.join(current_dir, 'data/LangId.test'), 'r', encoding='utf-8') as input_file, \
        open("output.txt", "w") as output_file:
        # calculate probability of each language for each line in test file
        for i, line in enumerate(input_file):
            probability_en = calculate_probability(line, unigrams_dict_en, bigrams_dict_en, total_vocab_cnt)
            probability_fr = calculate_probability(line, unigrams_dict_fr, bigrams_dict_fr, total_vocab_cnt)
            probability_it = calculate_probability(line, unigrams_dict_it, bigrams_dict_it, total_vocab_cnt)
            prob_dict = {probability_en: 'English', probability_fr: 'French', probability_it: 'Italian'}
            
            # for debugging purposes
            # print(f'i={i+1} en: {probability_en} fr: {probability_fr} it: {probability_it} max: {prob_dict[max(probability_en, probability_fr, probability_it)]}')
            
            # output with line number and predicted language
            output_file.write(f'{i+1} {prob_dict[max(probability_en, probability_fr, probability_it)]} \n')
            
    # print out accuracy and list of lines that were incorrect
    print(calculate_accuracy())
    
# calculates probability of language on a text using bigram probability with laplace smoothing
def calculate_probability(text, unigrams_dict, bigrams_dict, V):
    unigrams_test_text = word_tokenize(text)
    bigrams_test_text = list(ngrams(unigrams_test_text, 2))
    
    p_laplace = 1
    
    for bigram in bigrams_test_text:
        b = 0
        if bigram in bigrams_dict:
            b = bigrams_dict[bigram]
            
        u = 0
        if bigram[0] in unigrams_dict:
            u = unigrams_dict[bigram[0]]
        
        # multiply probabilities
        p_laplace = p_laplace * ((b + 1) / (u + V))
        
    return p_laplace

# calculates accuracy based on solution file and model predicted language in output.txt
def calculate_accuracy():
    correctly_classified_cnt = 0
    wrongly_classified_cnt = 0
    wrongly_classifed_lines_list = []
    
    # compare line by line of solution file and model output file
    with open("data/LangId.sol") as file1, open("output.txt") as file2: 
        for i, (x, y) in enumerate(zip(file1, file2)):
            if x.strip() == y.strip():
                correctly_classified_cnt += 1
            else:
                wrongly_classified_cnt += 1
                wrongly_classifed_lines_list.append(i + 1)
    
    accuracy = correctly_classified_cnt / (correctly_classified_cnt + wrongly_classified_cnt)
    return accuracy, wrongly_classifed_lines_list

if __name__ == "__main__":
    main()
