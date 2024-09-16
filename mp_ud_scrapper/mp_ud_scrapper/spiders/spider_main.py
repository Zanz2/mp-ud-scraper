import scrapy
from mp_ud_scrapper.items import MpUdScrapperItem
from mp_ud_scrapper.settings import SPLASH_REQ_ARGS
from scrapy_splash import SplashRequest

class MainSpider(scrapy.Spider):
    name = "main_spider"
    urls = [
            "https://www.politie.nl/gezocht-en-vermist/vermiste-volwassenen?page=1"
    ]

    def start_requests(self):
        for url in self.urls:
            yield SplashRequest(url=url, callback=self.parse, args=SPLASH_REQ_ARGS)
    
    def parse(self, response):
        #print(response.text)
        cases = response.css("get_all_cases")
        next_page = response.css("get_the_next_page")
        for case in cases:
                
            data = []
            
            "fill the data array hier with the case"
            
            item = MpUdScrapperItem()
            item["full_name"] = data
            item["missing_unidentified_since_time_date"] = data
            item["country_reported"] = data
            item["area"] = data
            item["case_text"] = data
            item["case_link"] = data
            yield item
            
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(next_page, callback=self.parse, args=SPLASH_REQ_ARGS)
