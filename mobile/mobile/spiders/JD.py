'''
@Description: 
@Autor: khuqen
@Date: 2020-01-05 14:12:19
@LastEditors  : khuqen
@LastEditTime : 2020-01-07 21:08:50
'''
# -*- coding: utf-8 -*-
import scrapy
from mobile.items import MobileItem
import requests
import time

class JdSpider(scrapy.Spider):
    name = 'JD'

    def __init__(self):

        self.page_num = 1

    def closed(self, spider):
        print("spider closed")

    def start_requests(self):
        start_urls = ['https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=1&s=1&click=0&scrolling=y']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # ids = response.css('li.gl-item::attr(data-sku)').getall()
        ids = response.css('li.ps-item a img::attr(data-sku)').getall()
        for id in ids:
            url = 'https://item.jd.com/{}.html'.format(id)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
        self.page_num = self.page_num + 1
        next_url = 'https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page={}&s={}&click=0&scrolling=y'.format(self.page_num, (1+(self.page_num-1)*30))
        if self.page_num <= 100:
            yield scrapy.Request(url=next_url, callback=self.parse)
        
    def parse_detail(self, response):
        name = response.css('ul.parameter2.p-parameter-list > li:nth-child(1)::attr(title)').get()
        store = response.css('#popbox > div > div.mt > h3 > a::attr(title)').get()
        ids = response.css('#choose-attr-2 > div.dd > div.item::attr(data-sku)').getall()
        values = response.css('#choose-attr-2 > div.dd > div.item::attr(data-value)').getall()
        for id, value in zip(ids, values):
            item = MobileItem()
            r = requests.get('https://p.3.cn/prices/mgets?skuIds=J_{}'.format(id))
            data = r.json()
            item['name'] = name + '#' + str(value)
            item['store'] = store
            item['price'] = data[0]['p']
            url = 'https://club.jd.com/comment/skuProductPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(id)
            headers = {
                'referer': 'https://item.jd.com/{}.html'.format(id)
            }
            r = requests.get(url, headers=headers)
            data = r.json()
            item['sales'] = data['productCommentSummary']['commentCount']
            yield item