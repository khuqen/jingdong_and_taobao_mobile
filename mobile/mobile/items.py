'''
@Description: 
@Autor: khuqen
@Date: 2020-01-05 14:11:28
@LastEditors  : khuqen
@LastEditTime : 2020-01-07 10:31:47
'''
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MobileItem(scrapy.Item):
 
    store = scrapy.Field()
    name = scrapy.Field()
    sales = scrapy.Field()
    price = scrapy.Field()
    
