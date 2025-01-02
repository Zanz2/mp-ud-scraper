import scrapy
from mp_ud_scraper.items import MpUdScraperItem
import json


class InterpolSpider(scrapy.Spider):
    name = "interpol_spider"
    
    def __init__(self, *args, **kwargs):
        super(InterpolSpider, self).__init__(*args, **kwargs)
        self.display_url = "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices"
        self.core_api_url = "https://ws-public.interpol.int/notices/v2/yellow"

        # It always returns only 160 results no matter the query, 
        # making it almost impossible to know all of the possible specific combinations to find all 10313 people on the site,
        # because you can only see 160 people at a time, no matter the query


    def start_requests(self):
        yield scrapy.Request(
            url=self.core_api_url,
            callback=self.parse
        )

    def parse(self, response):
        json_resp = response.json()
        dict_response = json.loads(json_resp)

        item = MpUdScraperItem()
            
        item["case_full_name"] = None
        item["case_missing_unidentified_since_time_date"] = None
        item["case_age"] = None
        item["case_area"] = None
        item["case_country_reported"] = None
        item["case_text"] = None
        item["case_link"] = None

        yield item
