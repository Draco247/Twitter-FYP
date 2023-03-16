import scrapy
from scrapy import Request,Spider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
# from twitterlinkscraper.twitterlinkscraper.items import TwitterlinkscraperItem
from twitterlinkscraper.items import TwitterlinkscraperItem
from scrapy.loader import ItemLoader
import mysql.connector
from readability import Document #For the Arc90 readability algorithm
import re
from scrapy import signals
import time
import os
import logging
import requests
from htmldate import find_date



class LinkscraperSpider(Spider):
    name = 'linkscraper'

   
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
    )
    curr = conn.cursor()
    # get all links to be crawled
    curr.execute("SELECT url_id,url FROM urltest")

    # curr.execute("SELECT urltest.url_id,url FROM urltest INNER JOIN to_crawl ON urltest.url_id = to_crawl.url_id LEFT JOIN crawled ON to_crawl.url_id = crawled.url_id WHERE crawled.url_id IS NULL")
    data = curr.fetchall()
    start_urls = []
    ids = []
    # print(data)
    # if data is None:
    #     os._exit(0)

    for i in data:
        id = i[0]
        # print(f"id = {id}")
        ids.append(i[0])
        start_urls.append(i[1])
    
    

    # def __init__(self, *args, **kwargs):
    #     logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
    #     logger.setLevel(logging.DEBUG)
    #     super().__init__(*args, **kwargs)
    
    def start_request(self):
        request = Request(url = self.start_urls)
        # request = Request(url = self.start_urls, callback=self.parse)
        yield request

    def parse(self,response):
        # print(f"hhrhrhr {self.urls}")
        # self.logger.getLogger('scrapy').setLevel(logging.WARNING)
        l = ItemLoader(item = TwitterlinkscraperItem(), selector = response)
        clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        doc = Document(response.text)
          
        
        response.follow(response.request.url, meta={'source_url': response.url})
        source_url = response.meta
        r = requests.head(response.url)
        
        url = response.request.url
        print(url)
        if 'redirect_urls' in source_url:
            # url = source_url['redirect_urls'][0]
            l.add_value('id', self.ids[self.start_urls.index(source_url['redirect_urls'][0])])
            # print(f"url = {source_url['redirect_urls'][0]}")
        else:
            # print()
            l.add_value('id', self.ids[self.start_urls.index(response.request.url)])
        l.add_value('title', re.sub(clean,'',doc.title()))
        # l.add_css('content', 'p')
        l.add_value('content',re.sub(clean,'',doc.summary().strip()))
        # article_date = response.css('time::attr(datetime)').get()
        l.add_value('date',find_date(url))
         
        yield l.load_item()


# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(LinkscraperSpider)
#     process.start()