# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Msg58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name=scrapy.Field()
    company=scrapy.Field()
    person_name=scrapy.Field()
    phone=scrapy.Field()
    work_place=scrapy.Field()
    phone_image_number=scrapy.Field()
