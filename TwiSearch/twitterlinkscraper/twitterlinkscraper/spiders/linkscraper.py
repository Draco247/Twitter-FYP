import scrapy
from scrapy import Request,Spider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
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
    host="placeholder",
    user="placeholder",
    password="placeholder",
    database="placeholder"
    )
    curr = conn.cursor()
    # get all links to be crawled
    curr.execute("SELECT url_id,url FROM urls")

    data = curr.fetchall()
    start_urls = []
    ids = []


    for i in data:
        id = i[0]
        ids.append(i[0])
        start_urls.append(i[1])
    
    def start_request(self):
        request = Request(url = self.start_urls)
        yield request

    def parse(self,response):
        l = ItemLoader(item = TwitterlinkscraperItem(), selector = response)
        clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        doc = Document(response.text)
          
        
        response.follow(response.request.url, meta={'source_url': response.url})
        source_url = response.meta
        r = requests.head(response.url)
        
        url = response.request.url
        print(url)
        if 'redirect_urls' in source_url:
            l.add_value('id', self.ids[self.start_urls.index(source_url['redirect_urls'][0])])
        else:
            l.add_value('id', self.ids[self.start_urls.index(response.request.url)])
        
        l.add_value('title', re.sub(clean,'',doc.title()))
        l.add_value('content',re.sub(clean,'',doc.summary().strip()))
        l.add_value('date',find_date(url))
         
        yield l.load_item()
