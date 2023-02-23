# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose,Join
from w3lib.html import remove_tags
from unidecode import unidecode

class TwitterlinkscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field(input_processor = MapCompose(remove_tags,unidecode), output_processor = TakeFirst())
    content = scrapy.Field(input_processor = MapCompose(remove_tags,unidecode,str.strip), output_processor = Join(' '))
    date1 = scrapy.Field()
    date2 = scrapy.Field()
    date3 = scrapy.Field()
