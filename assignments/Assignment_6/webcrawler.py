import requests
import urllib.request
import re
import pickle
from bs4 import BeautifulSoup
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

# main runner that calls other functions
def main():
    web_crawl()
    clean_text()
    extract_important_terms()
    build_knowledge_base()
    # debug_pickle()

# for debugging pickle 
def debug_pickle():
    kb = pickle.load(open('knowledge_base_dict.p', 'rb'))  
    for term in kb.keys():
        for fact in kb[term]:
            print(f"{term}: {fact}")
    # for k in kb['largest']:
    #     print(k)

# crawls from starter url, and gets 15 relevant urls that are outputted to urls.txt
def web_crawl():

    starter_url = "https://www.google.com/search?q=dallas&oq=dallas&aqs=chrome.0.69i59j69i57.1365j0j9&sourceid=chrome&ie=UTF-8"
    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, features='html.parser')

    urls_cnt = 0
    with open('urls.txt', 'w', encoding='utf-8') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            # print(link_str)
            if 'dallas' in link_str or 'Dallas' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('https') and 'google' not in link_str:
                    # test to see if url is accessible before writing to urls.txt
                    try:
                        req = urllib.request.Request(link_str, headers={'User-Agent': 'Mozilla/5.0'})
                        urllib.request.urlopen(req).read().decode('utf8')
                    except:
                        print("URL is not accesible. Skipping")
                    else:    
                        f.write(link_str + '\n')
                        urls_cnt += 1
                        if urls_cnt >= 15:
                            break
    print("Web crawling complete. Urls written to urls.txt")                     
# scrapes each url from urls.txt, cleans the text, tokenizes sentences, outputs
# to url{i}.txt, where i is the line number from urls.txt
def clean_text():
    
    with open('urls.txt', 'r', encoding='utf-8') as urls_file:
        # go through each url and scrape
        for i, url in enumerate(urls_file):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read().decode('utf8')
            soup = BeautifulSoup(html, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()

            # gets text from <p> tags, cleans them, and adds them to a list
            cleaned_text_list = []
            for p in soup.select('p'):
                p_text = p.get_text().strip()
                cleaned_text_list.append(re.sub("\[[\w\d\s]+\]", '', p_text))
                
            # sentence tokenize all the text from url
            sentences = sent_tokenize(" ".join(cleaned_text_list))
            
            # write out to file sentence by sentence
            with open(f'url{i+1}.txt', 'w', encoding='utf-8') as output_file:

                for sentence in sentences:
                    output_file.write(sentence + "\n")
                print(f"url{i+1}.txt written")
# does preprocessing, calculates term frequency (tf) value, and prints out top 25 terms 
def extract_important_terms():
    tf_dict = {}
    total_tokens_len = 0
    # go through each url file
    for i in range(1,16):
        with open(f'url{i}.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            
        # remove newline, tab, stop words
        processed_punct_text = re.sub(r'[.?!,:;()\-\n\d]',' ', text.lower())
        stop_words = set(stopwords.words('english'))


        tokens = word_tokenize(processed_punct_text)
        total_tokens_len += len(tokens)
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]

        # count term frequency
        for t in tokens:
            if t in tf_dict:
                tf_dict[t] += 1
            else:
                tf_dict[t] = 1
    
    # calculate term frequency
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / total_tokens_len
    
    # output top 40 terms in dict
    for key in sorted(tf_dict, key=tf_dict.get, reverse=True)[:40]:
        print(key, tf_dict[key])

# creates knowledge base using selected important terms and outputs knowledge base dictionary
# as pickle file
def build_knowledge_base():
    important_terms = ["city", "texas", "largest", "park", "district", "population", "station", "river", "north", "downtown"]
    knowledge_base_dict = defaultdict(list)
    
    # goes through all the url files sentence by sentence.
    # if a sentence contains term from important_terms list, add that sentence to knowledge base for that term
    for i in range(1,16):
        with open(f'url{i}.txt', 'r', encoding='utf-8') as f:
            for line in f:
                for term in important_terms:
                    if term in line.lower():
                        knowledge_base_dict[term].append(line.strip())
    
    # pickle knowledge base
    pickle.dump(knowledge_base_dict, open('knowledge_base_dict.p', 'wb'))
    print("Knowledge base pickled to knowledge_base_dict.p")
    
    return knowledge_base_dict

if __name__ == "__main__":
    main()
