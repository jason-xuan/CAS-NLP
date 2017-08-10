# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
from datetime import datetime
from scrapy import signals
from scrapy.exceptions import DropItem


class DropItemPipeline(object):

    def process_item(self, item, spider):
        if item['title'] == '':
            raise DropItem("Duplicate item found: %s" % item)
        if item['text'] == ' ':
            raise DropItem("Duplicate item found: %s" % item)
        return item

class News163JsonPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        # fieldnames = ['url', 'title', 'text']
        self.file = open('%s_%s_products.json' % (spider.name, str(datetime.now()).replace(':', '-')), 'w', encoding='utf-8')
        # self.csv = csv.DictWriter(self.file, fieldnames=fieldnames)
        # self.csv.writeheader()

    def spider_closed(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item['text'] = item['text'].replace('\n', ' ')
        j = {
            'url': item['url'],
            'source': item['source'],
            'title': item['title'],
            'text': item['text']
        }
        self.file.write(json.dumps(j))
        self.file.write('\n')
        return item

