# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MpUdScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    full_name = scrapy.Field()
    missing_unidentified_since_time_date = scrapy.Field()
    country_reported = scrapy.Field()
    area = scrapy.Field()
    case_text = scrapy.Field()
    case_link = scrapy.Field()

