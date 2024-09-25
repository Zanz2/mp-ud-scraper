import scrapy
from mp_ud_scraper.items import MpUdScraperItem
from datetime import datetime
import time
import asyncio
import logging 
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.WARNING)  # You can set to DEBUG, INFO, WARNING, etc.
logger1 = logging.getLogger('scrapy-playwright') 
logger1.setLevel(logging.WARNING)

logging.basicConfig(level=logging.WARNING)  # You can set to DEBUG, INFO, WARNING, etc.
logger1 = logging.getLogger('scrapy') 
logger1.setLevel(logging.WARNING)

zaginieni_matching_dict = { 
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div.content div.search_result_list div.item_wrap")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("p.search_result_pagination a.active[href] + a").attrib["href"].strip()),
    
    "case_full_name": (lambda case_css: case_css.css("span.info span.title::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("span.info span.date::text").get().strip().split(" ")[3], '%Y/%m/%d').strftime('%d/%m/%Y')),
    "case_age": (lambda case_css: case_css.css("span.info span.age::text").get().strip().lower().replace("years old","")),
    "case_area": (lambda case_css: case_css.css("span.info span.place strong::text").get().strip().lower().replace("last seen","").replace("poza granicami polski", "outside poland")),
    "case_country_reported": (lambda case_css: "Poland" ),
    "case_text": (lambda case_css: " | ".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall() if text_entry.strip() != ""])),
    "case_link": (lambda case_css: case_css.css("a[href]").attrib["href"].strip()),
}

class ZaginieniSpider(scrapy.Spider):
    name = "zaginieni_spider"
    
    def __init__(self, *args, **kwargs):
        super(ZaginieniSpider, self).__init__(*args, **kwargs)

        # The key for the dict is the url itself, the values are important attributes
        self.matching_dict = {
            "https://zaginieni.pl/search-results/?type=nn&height_from=&height_to=&age=now&age_from=&age_to=&eyes=&city=&district=": zaginieni_matching_dict,
            "https://zaginieni.pl/search-results/?firstname=&lastname=&type=missing&height_from=&height_to=&eyes=&age_from=&age_to=&age=now&city=&district=": zaginieni_matching_dict,
        }

    def start_requests(self):
        for url, attributes in self.matching_dict.items():
            #if url != "https://zaginieni.pl/search-results/?firstname=&lastname=&type=missing&height_from=&height_to=&eyes=&age_from=&age_to=&age=now&city=&district=": continue
            #if url != "https://zaginieni.pl/search-results/?type=nn&height_from=&height_to=&age=now&age_from=&age_to=&eyes=&city=&district=": continue
            yield scrapy.Request(url=url, meta={"playwright": True, "playwright_include_page": True}, callback=self.parse)
    
    def match_paginated_url_to_original(self, paginated_url):
        best_match = None
        best_match_length = 0
        all_urls = self.matching_dict.keys()
        for url in all_urls:

            end_index = min([len(paginated_url), len(url)])
            match_length = 0
            for index in range(end_index):
                if url[index] == paginated_url[index]: match_length += 1

            if match_length > best_match_length:
                best_match_length = match_length
                best_match = url
        return best_match


    async def parse(self, response):
        page = response.meta['playwright_page']
        url_attributes = self.matching_dict[self.match_paginated_url_to_original(response.url)]
        
        while True:
            print(f"Current page: {response.css('p.search_result_pagination a.active[href]::text').get().strip()}")
            cases = url_attributes["get_all_cases"](response)
            for case in cases:
        
                item = MpUdScraperItem()
                
                for attribute in url_attributes:
                    if "get" in attribute: continue # these are the functions to get all the cases and the next page, we ignore those
                    #if "text" not in attribute: continue # debug
                    try:
                        item[attribute] = url_attributes[attribute](case)
                    except Exception as e:
                        #if attribute == "": raise e # debug
                        item[attribute] = "N/a"

                yield item
            try:
                next_page = url_attributes["get_the_next_page"](response)
            except Exception as e:
                return 

            # Click on the "Next Page" button and wait for the page to load
            next_button_selector = 'p.search_result_pagination a.active[href] + a'  # Change this to match the "Next Page" button on your website
            while True:
                try:
                    await asyncio.sleep(0.1)
                    await page.click(next_button_selector)
                    await asyncio.sleep(0.1)
                    time.sleep(0.1)
                    await page.wait_for_load_state('networkidle')  # Wait until there are no network requests
                    await asyncio.sleep(0.1)

                    # Get the content of the new page
                    html_str = await page.content()
                    time.sleep(0.1)
                    response = scrapy.http.HtmlResponse(url=next_page, body=html_str, encoding='utf-8')
                    break
                except PlaywrightTimeoutError as e:
                    next_button_selector = 'p.search_result_pagination a.active[href]'
                    continue
                