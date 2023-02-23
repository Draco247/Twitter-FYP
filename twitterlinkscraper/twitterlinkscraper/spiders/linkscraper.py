import scrapy
from scrapy import Request,Spider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twitterlinkscraper.twitterlinkscraper.items import TwitterlinkscraperItem
# from twitterlinkscraper.items import TwitterlinkscraperItem
from scrapy.loader import ItemLoader
import mysql.connector
from readability import Document #For the Arc90 readability algorithm
import re
from scrapy import signals
import time

class LinkscraperSpider(Spider):
    name = 'linkscraper'

   
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ShadowSlash247",
    database="mydatabase"
    )
    curr = conn.cursor()
    data = ""
    while data == "":
        curr.execute("SELECT urltest.url_id,url from urltest JOIN to_crawl WHERE urltest.url_id = to_crawl.url_id")
        if curr.fetchall() != []:
            data = curr.fetchall()
        time.sleep(5)

    # print(ascii(data))
    start_urls = []
    ids = []
    for i in data[400:500]:
        id = i[0]
        # print(f"id = {id}")
        ids.append(i[0])
        start_urls.append(i[1])
    
    def start_request(self):
        request = Request(url = self.start_urls, callback=self.parse)
        yield request

    def parse(self,response):
        # print(f"hhrhrhr {self.urls}")
        l = ItemLoader(item = TwitterlinkscraperItem(), selector = response)
        clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        doc = Document(response.text)
        # print("*==============================*")
        iframe_elements = response.xpath('//iframe')
        video_urls = []
        for iframe in iframe_elements:
            src = iframe.xpath('@src').get()
            if src and 'youtube' in src:  # adjust this check for the specific video platform you're interested in
                video_urls.append(src)
        # print(video_urls)
        # print(re.sub(clean,'',doc.summary()))
        # # re.sub(clean,'',doc.title())
        # print("================================")
        # l.add_css('title', 'h1')
        response.follow(response.request.url, meta={'source_url': response.url})
        source_url = response.meta
        # print(f"yeep = {source_url}")
        # pages = self.stats.get_stats()
        # print(f"pages = {pages}")# need to get finish time as well
        if 'redirect_urls' in source_url:
            l.add_value('id', self.ids[self.start_urls.index(source_url['redirect_urls'][0])])
            # print(f"url = {source_url['redirect_urls'][0]}")
        else:
            # print()
            l.add_value('id', self.ids[self.start_urls.index(response.request.url)])
        l.add_value('title', re.sub(clean,'',doc.title()))
        # l.add_css('content', 'p')
        l.add_value('content',re.sub(clean,'',doc.summary().strip()))
        # article_date = response.css('time::attr(datetime)').get()
        l.add_css('date1','time::attr(datetime)')
        l.add_css('date2','meta[name="publish-date"]::attr(content)')
        # text_with_date = response.xpath('//p[contains(text(), "Published on")]').get()
        # article_date = re.search(r'(\d{4}-\d{2}-\d{2})', text_with_date).group(1)
        yield l.load_item()

        

        # self.results.append(l.load_item())


        # title = response.css("h1::text").get()
        # print(title)
        # item['title'] : response.css("h1::text").get()

        # print("--------------------------")
        # paragraphs = response.css("p")
        # for paragraph in paragraphs:
        #     l2 = ItemLoader(item = TwitterlinkscraperItem(), selector = paragraph)
        #     l2.add_css('content','p')
        #     yield l2.load_item()
            # item['content'] : paragraph.get()
           
            # print(paragraph)
        #     print("************************")
        # print("--------------------------")
        # pass
        


        # paragraphs = response.css("#main-content > div.ssrcss-1ocoo3l-Wrap.e42f8511 > div > div.ssrcss-rgov1k-MainColumn.e1sbfw0p0 > article > div.ssrcss-11r1m41-RichTextComponentWrapper.ep2nwvo0")
        # for paragraph in paragraphs:
        #     yield{
        #         'content' : paragraph.css("p").get(),
        #     }

# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(LinkscraperSpider)
#     process.start()