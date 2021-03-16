# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    small_area = scrapy.Field()
    area = scrapy.Field()
    location_desc = scrapy.Field()
    month_money = scrapy.Field()
    url = scrapy.Field()
