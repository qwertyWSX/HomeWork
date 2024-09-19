# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst


class ImagesItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
