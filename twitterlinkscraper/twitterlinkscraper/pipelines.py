# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import mysql.connector
from twitterlinkscraper.spiders.linkscraper import LinkscraperSpider
# from twitterlinkscraper.twitterlinkscraper.spiders.linkscraper import LinkscraperSpider

# from.spiders.linkscraper import LinkscraperSpider
from scrapy import signals
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
# import nltk
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
    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(LinkscraperSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signals.spider_closed)
    #     return spider

    # def spider_closed(self, spider):
    #     spider.logger.info('Spider closed: %s', spider.name)
    #     self.logger.info("Start time: %s", self.crawler.stats.get_stats())
    
    # def __init__(self, stats):
    # self.stats = stats

    # def ymdhms_to_timestamp(value: str) -> int:
    #     dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    #     return int(dt.timestamp())


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
        
        # text = stem_text(text) # stemming
        text = remove_special_characters(text) # remove punctuation and symbols
        text = remove_stopwords(text) # remove stopwords
        print(f"text is here {text}")
        text = detect_lang(text)
        if text != "Not English":
            text_dict = convert(text)
            return text_dict
        else:
            return ""
    
    def process_item(self, item, spider):
        # print(f"this is it: {item['id'][0]}")
        # print(f"here we are {self.clean_text(item['content'])}")
        sql = "INSERT INTO crawled (url_id,crawl_start) VALUES (%s,%s)"
        
        val = ([item['id'][0],self.stats.get_value('start_time')])
        self.curr.execute(sql, val)
        if item['title'] != ""  and item['content'] != "" and 'date' in item:
            title = item['title']
            words = item['content'].split()
            if len(words) > 20:
                new_string = ' '.join(words[:20]) + "...."
            else:
                new_string = ' '.join(words)
            description = new_string

            # dates = item['date']
            # iso_date = parse(dates[0]).isoformat()
            # print(f"dates = {dates}")
            # iso_dates = []
            # for date in dates:
            #     try:
            #         iso_date = parse(date).isoformat()
            #         print(f" hello fuckers {iso_date}")
            #         # iso_dates.append(iso_date)
            #     except ValueError:
            #         try:
            #             iso_date = datetime.fromtimestamp(int(date))
            #         except ValueError:
            #             pass

            # Get the most oldest date(most likely to be when first posted)
            # most_recent_date = min(iso_dates)

            text = self.clean_text(f"{item['title']} {item['content']}")
            if text != "":
                sql2 = "INSERT INTO text_words (url_id, title, description, words, date) VALUES (%s,%s,%s,%s,%s)"
                val2 = ([item['id'][0],title,description,text, item['date'][0]])
                self.curr.execute(sql2, val2)
            
        return item
    
    

    def open_spider(self, spider):
        self.curr = self.conn.cursor()
        # self.client = pymongo.MongoClient(self.mongo_uri)
        # self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.conn.commit()
        self.curr.close()
        self.conn.close()



    # def open_spider(self, spider):
    #     self.file = open('result.json', 'w')

    # def close_spider(self, spider):
    #     self.file.close()

    # def process_item(self, item, spider):
    #     print(f"Processing item: {self.stats.get_stats()}")
    #     line = json.dumps(dict(item)) + "\n"
    #     self.file.write(line)
    #     return item