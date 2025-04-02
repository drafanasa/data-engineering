# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class YelpItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    review_count = scrapy.Field()