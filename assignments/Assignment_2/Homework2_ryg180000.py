import sys
import os
import re
import nltk
import collections
import random

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# main function that calls text processing and run_game functions
def main():

    # require pathfile as a sys arg
    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
        text = process_file(arg_input)
        
        # get lexical diversity
        tokens = word_tokenize(text)
        print("Lexical diversity: " + '{:.2f}'.format(len(set(tokens)) / len(tokens)) + "\n")
        
        # call function to preprocess text, returns tokens and # of nouns from lemmas
        tokens_list, nouns_list = preprocess_text(text)
        
        nouns_dict = {}
        # create tokens counter dictionary in format of {token: count of token}
        tokens_counter = collections.Counter(tokens_list)
        # create entry in nouns_dict for each noun and its count from tokens counter dictionary
        for noun, _ in nouns_list:
            nouns_dict[noun] = tokens_counter[noun] 
        
        # sort by count in decreasing order, and store only first 50, and print
        sorted_most_common_nouns = dict(sorted(nouns_dict.items(), key=lambda item: item[1], reverse=True)[:50])
        print(f"Fifty most common words: {sorted_most_common_nouns} \n")
        
        run_game(list(sorted_most_common_nouns.keys()))
        
    else:
        print("Please enter the relative path to the data file as a sys arg")

# opens file and returns file contents as string
def process_file(filepath):

    current_dir = os.getcwd()
    with open(os.path.join(current_dir, filepath), 'r') as f:
        text = f.read()
    return text    

# preprocess text tokens 
def preprocess_text(text):
    # remove punctuation
    processed_punct_text = re.sub(r'[.?!,:;()\-\n\d]',' ', text.lower())
    stop_words = set(stopwords.words('english'))
    
    tokens = word_tokenize(processed_punct_text)
    
    # remove stopwords
    processed_tokens = [t for t in tokens if not t in stop_words and len(t) > 5]
    
    # lemmatize words and get unique lemmas
    wnl = WordNetLemmatizer()
    unique_lemmas = set([wnl.lemmatize(t) for t in processed_tokens])
    
    tags = nltk.pos_tag(unique_lemmas)
    # print first 20 tagged lemmas
    print(f"First 20 tagged lemmas: {tags[:20]} \n")
    
    # get POS tagging for lemmas that are nouns
    noun_lemmas = [lemma for lemma in tags if lemma[1] == 'NN']
    
    print(f"Number of tokens: {len(processed_tokens)}, Number of lemmas: {len(noun_lemmas)} \n")
    return (processed_tokens, noun_lemmas)

# runnable to start and run game. Parameters are word bank and default parameter of 5 for user score
def run_game(word_bank, user_score = 5):    
    
    # random index from 0 to 49 inclusive
    rand_idx = random.randint(0, len(word_bank)-1)
    rand_word = word_bank[rand_idx]

    print(rand_idx, rand_word)    
    # current status of displayed word
    current_word_status = ["_"] * len(rand_word)
    # keep track of how many letters in word are correctly guessed
    correct_letters = 0
    # keep track of which letters have been guessed
    guessed_letters = set()
    
    # keep game running
    while True:
        print("".join(current_word_status))
        user_guess = input("Guess a letter: ")
        
        if user_guess == "!":
            print(f"Ending game. Your final score was: {user_score}")
            break
        
        if not user_guess.isalpha():
            print("Please enter an alphabetical letter")
            continue
        
        if len(user_guess) > 1:
            print("Please guess a single alphabetical letter")
            continue
        
        if user_guess.lower() in guessed_letters:
            print("Already guessed that letter. Please guess a new letter")
            continue
        
        # if guessed letter not in word
        if user_guess.lower() not in rand_word:
            user_score -= 1
            guessed_letters.add(user_guess.lower())
            
            if user_score < 0:
                print(f"You were unable to solve the word. The word was: {rand_word}")
                break
            else:
                print(f"Sorry, guess again! Score is {user_score}")
                
        # correctly guessed a letter in word
        else:
            user_score += 1
            guessed_letters.add(user_guess.lower())
            
            print(f"Right! Score is {user_score}")
            
            # if user's guess matches a letter(s) in the current word,
            # update current_word_status display and add to # of correct letters
            for i in range(len(rand_word)):
                if rand_word[i].lower() == user_guess.lower():
                    current_word_status[i] = user_guess.lower()
                    correct_letters += 1

            # if all letters have been found, generate new random word from word bank, 
            # reset game variables and continue game
            if correct_letters == len(rand_word):
                print("".join(current_word_status))
                print(f"You solved it! Your score is: {user_score}")
                
                rand_idx = random.randint(0, len(word_bank)-1)
                rand_word = word_bank[rand_idx]
                current_word_status = ["_"] * len(rand_word)
                correct_letters = 0
                guessed_letters = set()
                
if __name__ == "__main__":
    main()
