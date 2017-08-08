# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()

    def __str__(self):
        return '<Item {0}>'.format(self['title'])

