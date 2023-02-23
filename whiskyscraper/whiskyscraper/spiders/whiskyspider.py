import scrapy
from whiskyscraper.items import WhiskyscraperItem

class WhiskySpider(scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            try:
                yield{
                'name': products.css('a.product-item-link').get(),
                'price':products.css('span.price').get(),
                'link': products.css('a.product-item-link::attr(href)').get(), 
                }
            except:
                 yield{
                    'name': products.css('a.product-item-link').get(),
                    'price':"sold out",
                    'link': products.css('a.product-item-link::attr(href)').get(), 
                }