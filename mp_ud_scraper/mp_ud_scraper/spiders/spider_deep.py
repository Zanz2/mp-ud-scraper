import scrapy
from mp_ud_scraper.items import MpUdScraperItem
from datetime import datetime

# Improvements that would be nice to have but require considerably more work:
# TODO improvement for some sites where list cards show less info: actually go into the card links and scrape the area and case text from there, its more robust

interpol_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#container").css("li")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("No pagination, this will and should fail")),
    "case_full_name": (lambda case_css: case_css.css("*::text").getall()[1].strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: case_css.css("*::text").getall()[-1].strip()),
    "case_age": (lambda case_css: case_css.css("*::text").getall()[-2].strip()),
    "case_area": (lambda case_css: "Area abbrev.: " + case_css.css("*::text").getall()[0].strip()[-3:]),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: case_css.css("a[href]").attrib["href"].strip()),
}

missingpeople_org_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#container").css("li")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("No pagination, this will and should fail")),
    "case_full_name": (lambda case_css: case_css.css("*::text").getall()[1].strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: case_css.css("*::text").getall()[-1].strip()),
    "case_age": (lambda case_css: case_css.css("*::text").getall()[-2].strip()),
    "case_area": (lambda case_css: "Area abbrev.: " + case_css.css("*::text").getall()[0].strip()[-3:]),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: case_css.css("a[href]").attrib["href"].strip()),
}


class DeepSpider(scrapy.Spider):
    name = "deep_spider"
    
    def __init__(self, *args, **kwargs):
        super(DeepSpider, self).__init__(*args, **kwargs)

        # The key for the dict is the url itself, the values are important attributes
        self.matching_dict = {
            "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices": interpol_matching_dict,
            # # For now skipping, would require parsing them case by case to get useful info, see the todo 
            "https://www.missingpeople.org.uk/appeal-search": missingpeople_org_matching_dict,
            "https://www.fbi.gov/wanted/kidnap": {}, # javascript, pages autoload
            "https://www.fbi.gov/wanted/vicap/unidentified-persons": {

            }, # javascript, pages autoload
            "https://www.fbi.gov/wanted/vicap/missing-persons": {

            }, # javascript, pages autoload with also a button to load them
        }

    def start_requests(self):
        for url, attributes in self.matching_dict.items():
            if url != "https://www.missingpeople.org.uk/appeal-search": continue
            yield scrapy.Request(url=url, callback=self.parse)
    
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


    def parse(self, response):
        url_attributes = self.matching_dict[self.match_paginated_url_to_original(response.url)]
        cases = url_attributes["get_all_cases"](response)
            
        for case in cases:
    
            item = MpUdScraperItem()
            
            for attribute in url_attributes:
                if "get" in attribute: continue # these are the functions to get all the cases and the next page, we ignore those
                #if "text" not in attribute: continue # debug

                try:
                    item[attribute] = url_attributes[attribute](case)
                except Exception as e:
                    if attribute == "": raise e # debug
                    item[attribute] = "N/a"

            yield item
        
        next_page = url_attributes["get_the_next_page"](response)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
