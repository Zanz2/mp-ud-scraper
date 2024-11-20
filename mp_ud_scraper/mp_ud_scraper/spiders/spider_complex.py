import scrapy
from mp_ud_scraper.items import MpUdScraperItem
from datetime import datetime


# THIS FILE IS UNFINISHED WORK IN PROGRESS
# Improvements that would make the links below work but require considerably more work:
# TODO sites where list cards show less info: actually go into the card links and scrape the area and case text from there, its more robust

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

missingpersonscenter_matching_dict = {
    "get_all_cases": (lambda scrapy_response: [case_selector for case_selector in scrapy_response.css("div.elementor-widget-jet-listing-grid div.elementor-widget-container div.jet-listing-grid__item[data-post-id]") if "active" in case_selector.css("::text").get().strip().lower() or "cold case" in case_selector.css("::text").get().strip().lower()]),
    

    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("ul.pagination li.go-next a[aria-label][href]").attrib["href"].strip()),
    "case_full_name": (lambda case_css: case_css.css("a h2::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("a p::text").get().strip().lower().replace("missing Since:",""), '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: "See link"),
    "case_area": (lambda case_css: "See link"),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.garda.ie" + case_css.css("a[href]").attrib["href"].strip()),
}

au_missingpersons_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("article#content div.missing-people li.missing-person")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("ul.pagination li.go-next a[aria-label][href]").attrib["href"].strip()),
    "case_full_name": (lambda case_css: case_css.css("a h2::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("a p::text").get().strip().lower().replace("missing Since:",""), '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: "See link"),
    "case_area": (lambda case_css: "See link"),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.garda.ie" + case_css.css("a[href]").attrib["href"].strip()),
}

uk_police_matching_dict = { # needs more in detail parsing
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#Main div.CaseGrid")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("div#Main p.Pagination a.Active + a[href]").attrib["href"].strip()),
    
    "case_full_name": (lambda case_css: case_css.css("th a[href]::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("td").getall()[0].attrib["data-sort-value"].strip(), '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: case_css.css("td::text").getall()[1].strip()),

    "case_area": (lambda case_css: case_css.css("td::text").getall()[2].strip()),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: case_css.css("td::text").getall()[3].strip()),
    "case_link": (lambda case_css: "https://en.wikipedia.org" + case_css.css("th a[href]").attrib["href"].strip()),
}

us_nam_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#Main div.CaseGrid")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("div#Main p.Pagination a.Active + a[href]").attrib["href"].strip()),
    
    "case_full_name": (lambda case_css: case_css.css("th a[href]::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("td").getall()[0].attrib["data-sort-value"].strip(), '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: case_css.css("td::text").getall()[1].strip()),

    "case_area": (lambda case_css: case_css.css("td::text").getall()[2].strip()),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: case_css.css("td::text").getall()[3].strip()),
    "case_link": (lambda case_css: "https://en.wikipedia.org" + case_css.css("th a[href]").attrib["href"].strip()),
}

class ComplexSpider(scrapy.Spider):
    name = "complex_spider"
    
    def __init__(self, *args, **kwargs):
        super(ComplexSpider, self).__init__(*args, **kwargs)

        # The key for the dict is the url itself, the values are important attributes
        self.matching_dict = {
            "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices": interpol_matching_dict,
            # # For now skipping, would require parsing them case by case to get useful info, see the todo (no info on cards)
            "https://www.missingpeople.org.uk/appeal-search": missingpeople_org_matching_dict, # no info on cards
            "https://www.fbi.gov/wanted/kidnap": {}, # javascript, pages autoload
            "https://www.fbi.gov/wanted/vicap/unidentified-persons": {

            }, # javascript, pages autoload
            "https://www.fbi.gov/wanted/vicap/missing-persons": {

            }, # javascript, pages autoload with also a button to load them
            "https://missingpersonscenter.org/latest-updates/": missingpersonscenter_matching_dict, # this site and pagination runs on javascript
            "https://www.missingpersons.gov.au/view-all-profiles": au_missingpersons_matching_dict, # no info on cards, website blank on first load, needed refresh
            "https://www.missingpersons.police.uk/en-gb/case-search/?page=1&orderBy=dateDesc ": uk_police_matching_dict, # no info on cards, needs deep parsing
            "https://www.namus.gov/MissingPersons/Search#/results": us_nam_matching_dict, # this and the 2 below are all a running on javascript and a bit different, so you cant just use 1 dict
            "https://www.namus.gov/UnidentifiedPersons/Search#/results": us_nam_matching_dict,
            "https://www.namus.gov/UnclaimedPersons/Search#/results": us_nam_matching_dict,
        }

    def start_requests(self):
        for url, attributes in self.matching_dict.items():
            if url != "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices": continue
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
