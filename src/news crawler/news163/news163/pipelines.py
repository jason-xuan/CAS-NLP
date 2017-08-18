# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
from datetime import datetime
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem


class DropItemPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        name = '{0}_{1}'.format(spider.name, str(datetime.now()).replace(':', '-'))
        self.file = open('{0}_drop_urls.json'.format(name) , 'w', encoding='utf-8')

    def spider_closed(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['title'] == '':
            self.file.write(json.dumps({
                    'reason': 'no title',
                    'url': item['url']
                }) + '\n')
            raise DropItem("empty item found: %s" % item)

        if item['text'] == ' ':
            self.file.write(json.dumps({
                    'reason': 'no text',
                    'url': item['url']
                }) + '\n')
            raise DropItem("empty item found: %s" % item)

        if item['text'] == '':
            self.file.write(json.dumps({
                    'reason': 'text is empty',
                    'url': item['url']
                }) + '\n')
            raise DropItem("empty item found: %s" % item)

        return item

class News163JsonPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        name = '{0}_{1}'.format(spider.name, str(datetime.now()).replace(':', '-'))
        self.file = open('{0}_products.json'.format(name) , 'wb')
        self.exporter = JsonLinesItemExporter(self.file)

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
