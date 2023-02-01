## What the program does
The program takes in a data file consisting of the first, middle, last name, id, and phone number of an
employee and does basic text processing to format the data into a Person object. If an id or phone number is not valid during
processing, the user must input a new, valid replacement.

When formatting is complete, the Persons objects are put into a dictionary and pickled into a byte stream, which can always
be unpickled in order to read the data.

## How to run it
Download the python program and have it in the same directory as a folder named `data`, which contains `data.csv`.
Run the python program with the system argument `data/data.csv`, denoting the relative path to the data file

## Strengths and weaknesses of Python for text processing
Python has many powerful built in and external libraries to help with text processing. It is very easy to work with strings and csv files
and the flexibility of the language makes it fast to get started without much boilerplate. Python is usually the go to for text processing for many people, but some weakness could include slower processing speed for bigger data sets and the simpler syntax making it easier to make mistakes and harder to debug.

## Lessons learned
I learned about the usefulness of serializing/pickling data to have easy disk access to data. This way, we would only need to process the data
once and save it for later viewing, rather than run the program each time to get the results. I was also able to get a general refresher on
working with the extensive string libraries in Python. Using built in functions like `capitalize()` and `lower()` made string processing trivial.