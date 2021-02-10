# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class NewsItem(scrapy.Item):
    headline = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    published_at = scrapy.Field()