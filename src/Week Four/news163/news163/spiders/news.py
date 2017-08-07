# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import News163Item


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']
    # rules = [Rule(LinkExtractor(allow='http://news.163.com*'), callback='parse_news')]
    #          Rule(LinkExtractor(allow='/song\?id=\d+'), callback="parse_song")]

    def parse(self, response):
        urls = response.xpath("//a[re:test(@href, 'http://news.163.com/\d+/\d+/\d+/*')]/@href").extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_news)

        # urls = response.xpath("//a[re:test(@href, 'http://news.163.com/*')]/@href").extract()
        # for url in urls:
        #     yield scrapy.Request(url, callback=self.parse)

    def parse_news(self, response):
        item = News163Item()
        item['url'] = response.url
        item['title'] = ''.join(response.xpath("//div[@class='post_content_main']/h1/text()").extract())
        item['text'] = '\n'.join(response.xpath("//div[@class='post_text']/p/text()").extract())
        yield item

        urls = response.xpath("//a[re:test(@href, 'http://news.163.com/\d+/\d+/\d+/*')]/@href").extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_news)


