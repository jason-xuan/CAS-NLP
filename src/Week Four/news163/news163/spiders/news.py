# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem


class NeteaseNewsSpider(CrawlSpider):
    name = 'netease'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com']
    rules = [Rule(LinkExtractor(allow=[r'(http://news\.163\.com)/(\d{2})/(\d{4})/\d+/(\w+)\.html']), 'parse_news')]

    def parse_news(self, response):

        item = NewsItem()
        item['url'] = response.url
        item['source'] = 'netease'
        item['title'] = ''.join(response.xpath("//div[@class='post_content_main']/h1/text()").extract())
        item['text'] = '\n'.join(response.xpath("//div[@class='post_text']/p/text()").extract())
        yield item


class SinaNewsSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn']
    rules = [Rule(LinkExtractor(allow=[r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(\d{4}-\d{2}-\d{2})/\d{4}(\d{8})\.(?:s)html']), 'parse_news')]

    def parse_news(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['source'] = 'sina'
        item['title'] = ''.join(response.xpath('//div[@class="page-header"]/h1/text()').extract())
        item['text'] = ' '.join(response.xpath('//div[@class="article article_16"]/p/text()').extract()).replace('\u3000', '')
        yield item


class TencentNewsSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['news.qq.com']
    start_urls = [
        'http://news.qq.com',
        'http://news.qq.com/articleList/rolls/',
        'http://news.qq.com/world_index.shtml',
        'http://society.qq.com/',
        'http://mil.qq.com/',
        'http://history.news.qq.com/',
        'http://cul.qq.com/',
        'http://gy.qq.com/',
        'http://gongyi.qq.com/',
        'http://ly.qq.com/',
        'http://news.qq.com/zt2015/wxghz/index.htm'
    ]
    rules = [Rule(LinkExtractor(allow=[r'(.*)/a/(\d{8})/(\d+)\.htm']), 'parse_news')]

    def parse_news(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['source'] = 'tencent'
        item['title'] = ''.join(response.xpath('//div[@class="hd"]/h1/text()').extract())
        item['text'] = ' '.join(response.xpath('//div[@class="bd"]/div/p/text()').extract())
        yield item