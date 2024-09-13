# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    publisher = scrapy.Field()
    price = scrapy.Field()
    ISBN = scrapy.Field()
    pages = scrapy.Field()
    year = scrapy.Field()
    pass
