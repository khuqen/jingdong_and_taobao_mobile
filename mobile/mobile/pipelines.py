'''
@Description: 
@Autor: khuqen
@Date: 2020-01-05 14:11:28
@LastEditors  : khuqen
@LastEditTime : 2020-01-07 10:33:11
'''
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
class MobilePipeline(object):
    def open_spider(self, spider):
        try:
            self.file = open('JDMobileData.csv', 'w', newline='',encoding='utf-8')
        except Exception as err:
            print(err)
        self.w = csv.writer(self.file)
        self.w.writerow(['store', 'name', 'sales', 'price'])

    def process_item(self, item, spider):
        
        self.w.writerow([item['store'], item['name'], item['sales'], item['price']])
        return item
    
    def close_spider(self, spider):
        self.file.close()
