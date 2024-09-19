import scrapy
from mp_ud_scraper.items import MpUdScraperItem
from mp_ud_scraper.settings import SPLASH_REQ_ARGS
from scrapy_splash import SplashRequest
from difflib import SequenceMatcher
from datetime import datetime

class MainSpider(scrapy.Spider):
    name = "main_spider"
    # The key for the dict is the url itself, the values are important attributes
    matching_dict = {
    "https://www.politie.nl/gezocht-en-vermist/vermiste-volwassenen?page=1": {
        "get_all_cases": (lambda scrapy_response: scrapy_response.css("ul.imagelist").css("li.content-gutter")),
        "get_the_next_page": (lambda scrapy_response: scrapy_response.css("a[rel='next']").attrib["href"]),
        "case_full_name": (lambda case_css: case_css.css("article").css("h3::text").get().strip()),
        "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("article").css("time[datetime]::text").get().strip(), '%d-%m-%Y').strftime('%d/%m/%Y')),
        "case_country_reported": (lambda case_css: "Netherlands"),
        "case_area": (lambda case_css: case_css.css("p::text").extract()[-1].strip()),
        "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add => if text_entry.split()
        "case_link": (lambda case_css: case_css.css("a.imagelistlink").attrib["href"].strip()),
    },
    "https://www.politie.nl/gezocht-en-vermist/vermiste-kinderen": {

    },
    "https://www.politie.be/opsporingen/nl/opsporingen/vermiste-personen": {

    },
    "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices": {

    },
    "https://www.doenetwork.org/mp-geo-euro-males.php": {

    }, # no pages
    "https://www.doenetwork.org/mp-geo-euro-females.php": {

    }, # no pages
    "https://zaginieni.pl/search-results/?firstname=&lastname=&type=missing&height_from=&height_to=&eyes=&age_from=&age_to=&age=now&city=&district=": {

    },
    "https://www.missingpeople.org.uk/appeal-search": {

    },
    "https://www.garda.ie/en/missing-persons/": {

    },
    #"https://www.ie.missingkids.com/" # website cannot be reached DNS error
    "https://www.fbi.gov/wanted/kidnap": {

    }, # javascript, pages autoload
    "https://www.fbi.gov/wanted/vicap/missing-persons": {

    }, # javascript, pages autoload with also a button to load them
    "https://missingpersonscenter.org/latest-updates/": {

    },
    "https://www.missingpersons.gov.au/view-all-profiles": {

    }, # website blank on first load, needed refresh
    "https://www.police.govt.nz/missing-persons/missing-persons-list": {

    },
    #"https://www.oic.icmp.int/index.php" # website cannot be reached DNS error
    "https://www.wikipedia.org/wiki/List_of_people_who_disappeared_mysteriously:_1990%E2%80%93present": {

    }, # wikipedia doesnt do pagination
    "https://www.politie.nl/gezocht-en-vermist/niet-geidentificeerde-personen?page=1": {

    },
    #"https://www.interpol.int/How-we-work/Notices/Operation-Identify-Me" # website currently unavailable internal error
    "https://www.missingpersons.police.uk/en-gb/case-search/?page=1&orderBy=dateDesc ": {

    },
    "https://www.namus.gov/dashboard?nocache=": {

    }, # missing / unidentified / unclaimed in separate pages with gallery option
    "https://www.fbi.gov/wanted/vicap/unidentified-persons": {

    }, # javascript, pages autoload
}

    def start_requests(self):
        for url, attributes in self.matching_dict.items():
            if url != "https://www.politie.nl/gezocht-en-vermist/vermiste-volwassenen?page=1": break
            #yield SplashRequest(url=url, callback=self.parse, args=SPLASH_REQ_ARGS)
            yield scrapy.Request(url=url, callback=self.parse)
    
    def match_paginated_url_to_original(self, paginated_url):
        best_match = None
        best_match_ratio = 0
        all_urls = self.matching_dict.keys()
        for url in all_urls:
            match_ratio = SequenceMatcher(None, paginated_url, url).ratio()
            if match_ratio > best_match_ratio:
                best_match_ratio = match_ratio
                best_match = url
        return best_match


    def parse(self, response):
        url_attributes = self.matching_dict[self.match_paginated_url_to_original(response.url)]
        cases = url_attributes["get_all_cases"](response)
        next_page = url_attributes["get_the_next_page"](response)
        for case in cases:
    
            item = MpUdScraperItem()

            for attribute in url_attributes:
                if "get" in attribute: continue # these are the functions to get all the cases and the next page, we ignore those
                #if "text" not in attribute: continue # debug
                try:
                    item[attribute] = url_attributes[attribute](case)
                except Exception as e:
                    #raise e # debug
                    item[attribute] = "N/a"

            yield item
            
        if next_page is not None:
            next_page = response.urljoin(next_page)
            #yield SplashRequest(next_page, callback=self.parse, args=SPLASH_REQ_ARGS)
            yield scrapy.Request(next_page, callback=self.parse)
