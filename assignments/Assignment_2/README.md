## What the program does
The program takes a file containing an excerpt from an anatomy textbook and performs text processing to create a word guessing game.
Using the NLTK library, we print the text's lexical diversity, tokenize the text, do POS tagging, and check for unique noun lemmas that will be used as a word bank to the guessing game.
The player starts with a score of 5 and gets a point for every correct guess, and the game continues until they either quit or reach a score of less than 0

## How to run it
Download the python program and have it in the same directory as your file 'anat19.txt'.
Run the python program with the system argument `anat19.txt` as the file path

## Lessons learned
I learned about various NLP and Python tools to clean and preprocess text, and to also perform basic NLP tasks like POS tagging and lemmatization.