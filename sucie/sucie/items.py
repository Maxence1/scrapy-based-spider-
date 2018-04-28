# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SucieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    district = scrapy.Field()
    date = scrapy.Field()
    maxPrice = scrapy.Field()
    minPrice = scrapy.Field()


