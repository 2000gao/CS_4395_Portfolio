import sys
import os
import re
import pickle

# Person class
class Person:
    
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
        
    def display(self):
        print("Employee id: ", self.id)
        print(f"\t{self.first} {self.mi} {self.last}")
        print(f"\t{self.phone}")

# Main runnable that checks for the sys arg path to the data file, calls function to process data file contents,
# pickles the processed Persons list, and then unpickles and calls display() to print to console
def main():

    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
        processed_persons_dict = process_file(arg_input)
        
        # Pickle the data to "dict.p"
        pickle.dump(processed_persons_dict, open('dict.p', 'wb'))
        
        print("Employee list: \n")
        
        # Unpickle the data and call each Person's display()
        for x in pickle.load(open('dict.p', 'rb')):
            processed_persons_dict[x].display()
        
    else:
        print("Please enter the relative path to the data file as a sys arg")


# Handles the file path and passes lines after the header to be formatted into Person objects
def process_file(filepath):

    current_dir = os.getcwd()
    with open(os.path.join(current_dir, filepath), 'r') as f:
        text_in = f.readlines()[1:]
    return format_content(text_in)    

# Formats the names, ids, and phone numbers of each line and stores formatted Person in persons_dictionary
def format_content(content):
    
    persons_dictionary = {}
    
    for line in content:
        stripped_line = line.replace('\n', '')
        text_variables = stripped_line.split(",")
        formatted_last_name = text_variables[0].lower().capitalize()
        formatted_first_name = text_variables[1].lower().capitalize()
        formatted_mid_name = text_variables[2].capitalize()
        
        # If no middle name, default to "X"
        if not text_variables[2]:
            formatted_mid_name = "X"
            
        formatted_id = format_id(text_variables[3])
        formatted_phone_number = format_phone_number(text_variables[4])   
         
        persons_dictionary[formatted_id] = Person(formatted_last_name, formatted_first_name, formatted_mid_name, formatted_id, formatted_phone_number)
        
    return persons_dictionary

# Checks if id follows rules, if not, will continue asking for valid id and returns formatted id
def format_id(id):
    formatted_id = id
    
    while not re.search('^([a-zA-Z]{2})([0-9]{4})$', formatted_id):
        print(f'ID is invalid: {id}\nID is two letters followed by 4 digits')
        formatted_id = input('Please enter a valid id: ')
        print("-" * 16)
    return formatted_id
    
# Checks if phone # follows rules, if not, will continue asking for valid phone # and returns formatted phone #
def format_phone_number(phone_number):
    formatted_phone_number = phone_number
    
    while not re.search('^([0-9]{3})-([0-9]{3})-([0-9]{4})$', formatted_phone_number):
        print(f'Phone {phone_number} is invalid\nEnter phone number in form 123-456-7890')
        formatted_phone_number = input('Enter phone number: ')
        print("-" * 16)
    return formatted_phone_number
        

if __name__ == "__main__":
    main()
