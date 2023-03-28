from itemadapter import ItemAdapter
import json
import mysql.connector
from twitterlinkscraper.spiders.linkscraper import LinkscraperSpider
from scrapy import signals
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from nltk.stem import PorterStemmer
import re
import json
from datetime import datetime
from dateutil.parser import parse
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import spacy

# nltk.download('punkt')
default_stemmer = PorterStemmer()
default_stopwords = stopwords.words('english')

class TwitterlinkscraperPipeline:

    def __init__(self, stats):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ShadowSlash247",
            database="mydatabase"
            )
        self.stats = stats
        
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
    
    def clean_text(self,text):
        def get_lang_detector(nlp, name):
            return LanguageDetector()
        
        nlp = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        nlp.add_pipe('language_detector', last=True)

        def detect_lang(text):
            doc = nlp(text)

            if doc._.language['language'] == 'en':
                return text
            else:
                return "Not English"
            
        def tokenize_text(text):
            return [w for s in sent_tokenize(text) for w in word_tokenize(s)]

        def remove_special_characters(text, characters=string.punctuation.replace('!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n', ' ')):
            tokens = tokenize_text(text)
            pattern = re.compile('[{}]'.format(re.escape(characters)))
            return ' '.join(filter(None, [pattern.sub('', t) for t in tokens]))

        def stem_text(text, stemmer=default_stemmer):
            tokens = tokenize_text(text)
            return ' '.join([stemmer.stem(t) for t in tokens])

        def remove_stopwords(text, stop_words=default_stopwords):
            tokens = [w for w in tokenize_text(text) if w not in stop_words]
            return ' '.join(tokens)
        
        def convert(text):
            dict = {}
            for i in text.split():
                # print(f"i is hello: {i}")
                if i in dict: 
                    dict.update({i: dict[i]+1})
                else:
                    dict[i] = 1
            json_object = json.dumps(dict, indent = 4) 
            return json_object

        text = text.strip(' ') # strip whitespaces
        text = text.lower() # lowercase
        
        text = remove_special_characters(text) # remove punctuation and symbols
        text = remove_stopwords(text) # remove stopwords
        text = detect_lang(text) #check if text is in English
        if text != "Not English":
            text_dict = convert(text)
            return text_dict
        else:
            return ""
    
    def process_item(self, item, spider):        
        if item['title'] != ""  and item['content'] != "" and 'date' in item:
            title = item['title']
            words = item['content'].split()
            if len(words) > 20:
                new_string = ' '.join(words[:20]) + "...."
            else:
                new_string = ' '.join(words)
            description = new_string

            text = self.clean_text(f"{item['title']} {item['content']}")
            if text != "":
                sql2 = "INSERT INTO text_words (url_id, title, description, words, date) VALUES (%s,%s,%s,%s,%s)"
                val2 = ([item['id'][0],title,description,text, item['date'][0]])
                self.curr.execute(sql2, val2)
            
        return item
    
    

    def open_spider(self, spider):
        self.curr = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.curr.close()
        self.conn.close()
