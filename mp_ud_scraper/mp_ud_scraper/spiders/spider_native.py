import scrapy
from mp_ud_scraper.items import MpUdScraperItem
from datetime import datetime
from dateutil import parser

# Improvements that would be nice to have but require considerably more work:
# TODO improvement for some sites where list cards show less info: actually go into the card links and scrape the area and case text from there, its more robust

politie_nl_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("ul.imagelist li.content-gutter")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("a[href][rel='next']").attrib["href"]),
    "case_full_name": (lambda case_css: case_css.css("article h3::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("article time[datetime]::text").get().strip(), '%d-%m-%Y').strftime('%d/%m/%Y')),
    "case_age": (lambda case_css: case_css.css("p.leeftijd::text").get().strip()),
    "case_country_reported": (lambda case_css: "Netherlands"),
    "case_area": (lambda case_css: case_css.css("p::text").extract()[-1].strip()),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.politie.nl" + case_css.css("a.imagelistlink").attrib["href"].strip()),
}
politie_be_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#block-mainpagecontent div.view-content div.item-list ul div.content")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("ul a[href][rel='next']").attrib["href"]),
    "case_full_name": (lambda case_css: case_css.css("h2 span.field--name-title a::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(case_css.css("div.field--type-datetime time.datetime[datetime]::text").get().strip(), '%d.%m.%Y').strftime('%d/%m/%Y')),
    "case_age": (lambda case_css: case_css.css("div.field--name-field-wanted-age div.field--item::text").get().strip()),
    "case_country_reported": (lambda case_css: "Belgium"),
    "case_area": (lambda case_css: case_css.css("div.field--name-field-wanted-combined-cities div.field--item::text").get().strip()),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.politie.be" + case_css.css("h2 span.field--name-title a").attrib["href"].strip()),
}
doe_network_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("div#container li")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("No pagination, this will and should fail")),
    "case_full_name": (lambda case_css: case_css.css("*::text").getall()[1].strip()),
    #datetime.strptime(str(parser.parse(case_css.css("*::text").getall()[-1].strip(), fuzzy=True))[:10], '%Y-%m-%d').strftime('%d/%m/%Y')
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(str(parser.parse(case_css.css("*::text").getall()[-1].strip(), fuzzy=True))[:10], '%Y-%m-%d').strftime('%d/%m/%Y')),
    #"case_missing_unidentified_since_time_date": (lambda case_css: case_css.css("*::text").getall()[-1].strip()),
    "case_age": (lambda case_css: case_css.css("*::text").getall()[-2].strip()),
    "case_area": (lambda case_css: "Area abbrev.: " + case_css.css("*::text").getall()[0].strip()[-3:]),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: case_css.css("a[href]").attrib["href"].strip()),
}

garda_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("article#content div.missing-people li.missing-person")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("ul.pagination li.go-next a[aria-label][href]").attrib["href"].strip()),
    "case_full_name": (lambda case_css: case_css.css("a h2::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(str(parser.parse(case_css.css("a p::text").get().strip().lower().replace("missing Since:",""), fuzzy=True))[:10], '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: "See link"),
    "case_area": (lambda case_css: "See link"),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.garda.ie" + case_css.css("a[href]").attrib["href"].strip()),
}

missingpersonscenter_matching_dict = {
    "get_all_cases": (lambda scrapy_response: scrapy_response.css("article#content div.missing-people li.missing-person")),
    "get_the_next_page": (lambda scrapy_response: scrapy_response.css("ul.pagination li.go-next a[aria-label][href]").attrib["href"].strip()),
    "case_full_name": (lambda case_css: case_css.css("a h2::text").get().strip()),
    "case_missing_unidentified_since_time_date": (lambda case_css: datetime.strptime(str(parser.parse(case_css.css("a p::text").get().strip().lower().replace("missing Since:",""), fuzzy=True))[:10], '%Y-%m-%d').strftime('%d/%m/%Y')),   
    "case_age": (lambda case_css: "See link"),
    "case_area": (lambda case_css: "See link"),
    "case_country_reported": (lambda case_css: "See link" ),
    "case_text": (lambda case_css: "|".join([ text_entry.strip() for text_entry in case_css.css("*::text").getall()])), # to skip empty strings add --> if text_entry.split()
    "case_link": (lambda case_css: "https://www.garda.ie" + case_css.css("a[href]").attrib["href"].strip()),
}


class NativeSpider(scrapy.Spider):
    name = "native_spider"
    
    def __init__(self, *args, **kwargs):
        super(NativeSpider, self).__init__(*args, **kwargs)

        # The key for the dict is the url itself, the values are important attributes
        self.matching_dict = {
            "https://www.politie.nl/gezocht-en-vermist/vermiste-volwassenen?page=1": politie_nl_matching_dict,
            "https://www.politie.nl/gezocht-en-vermist/vermiste-kinderen?page=1": politie_nl_matching_dict,
            "https://www.politie.nl/gezocht-en-vermist/niet-geidentificeerde-personen?page=1": politie_nl_matching_dict,
            "https://www.politie.be/opsporingen/nl/opsporingen/vermiste-personen": politie_be_matching_dict,
            #"https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices": 
            # # For now skipping, would require parsing them case by case to get useful info, see the todo 
            "https://www.doenetwork.org/mp-geo-euro-males.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-euro-females.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-aus-males.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-aus-females.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-mexico-males.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-mexico-females.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-canada-males.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-canada-females.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-us-males.php": doe_network_matching_dict, # no pages
            "https://www.doenetwork.org/mp-geo-us-females.php": doe_network_matching_dict, # no pages
            "https://www.garda.ie/en/missing-persons/": garda_matching_dict,
            #"https://www.ie.missingkids.com/" # website cannot be reached DNS error
            "https://missingpersonscenter.org/latest-updates/": missingpersonscenter_matching_dict,
            "https://www.missingpersons.gov.au/view-all-profiles": {

            }, # website blank on first load, needed refresh
            "https://www.police.govt.nz/missing-persons/missing-persons-list": {

            },
            #"https://www.oic.icmp.int/index.php" # website cannot be reached DNS error
            "https://www.wikipedia.org/wiki/List_of_people_who_disappeared_mysteriously:_1990%E2%80%93present": {

            }, # wikipedia doesnt do pagination
            #"https://www.interpol.int/How-we-work/Notices/Operation-Identify-Me" # website currently unavailable internal error
            "https://www.missingpersons.police.uk/en-gb/case-search/?page=1&orderBy=dateDesc ": {

            },
            "https://www.namus.gov/dashboard?nocache=": {

            }, # missing / unidentified / unclaimed in separate pages with gallery option
        }

    def start_requests(self):
        for url, attributes in self.matching_dict.items():
            if url != "https://missingpersonscenter.org/latest-updates/": continue
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
                    if attribute == "case_missing_unidentified_since_time_date": raise e # debug
                    item[attribute] = "N/a"

            yield item
        
        next_page = url_attributes["get_the_next_page"](response)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)