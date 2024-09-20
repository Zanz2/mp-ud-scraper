# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MpUdScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    case_full_name = scrapy.Field()
    case_missing_unidentified_since_time_date = scrapy.Field()
    case_age = scrapy.Field()
    case_country_reported = scrapy.Field()
    case_area = scrapy.Field()
    case_text = scrapy.Field()
    case_link = scrapy.Field()

