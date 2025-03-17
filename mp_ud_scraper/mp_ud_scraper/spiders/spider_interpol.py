import scrapy
from mp_ud_scraper.items import MpUdScraperItem
import datetime
import time
from dateutil import parser

class InterpolSpider(scrapy.Spider):
    name = "interpol_spider"
    
    def __init__(self, *args, **kwargs):
        super(InterpolSpider, self).__init__(*args, **kwargs)
        self.display_url = "https://www.interpol.int/en/How-we-work/Notices/Yellow-Notices/View-Yellow-Notices"
        self.core_api_url = "https://ws-public.interpol.int/notices/v2/yellow"

        # NOTE:
        # It always returns only 160 results no matter the query, 
        # making it almost impossible to know all of the possible specific combinations to find all 10313 people on the site,
        # because you can only see 160 people at a time, no matter the query

        # Solution:
        # so the approach is to query per day the missing person was reported, and hopefully there were never more than 160 persons reported on a single day (not robust)
        # However, it still appears that only 1/5 of the data is visible to me, the rest might be disabled for the general public?

    def start_requests(self):
        yield scrapy.Request(
            url=self.display_url,
            callback=self.parse
        )

    def calculate_age(self, birthdate):
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def parse_entries(self, response):
        json_resp = response.json()
        if response.status == 403:
            raise Exception('Received 403 error')
        if len(json_resp["_embedded"]["notices"]) > 157: # PROBABLY MORE THAN 160 HITS ON URL
            with open("interpol_log/too_big_requests.txt", "a") as file:
                file.write(f"{response.url} \n")
                print("MORE THAN 160 HITS ON URL")

        for notice in json_resp["_embedded"]["notices"]:
            print(notice)
            item = MpUdScraperItem()
            
            name_str = ""
            if notice["forename"]: 
                name_str += notice["forename"]
            if notice["name"]:
                name_str += " "
                name_str += notice["name"]

            if name_str == "":
                name_str = "UNKNOWN"

            item["case_full_name"] = name_str
            
            item["case_missing_unidentified_since_time_date"] = datetime.datetime.strptime(str(parser.parse(notice["date_of_event"], fuzzy=True))[:10], '%Y-%m-%d').strftime('%d/%m/%Y')
            try:
                birthdate_object = datetime.datetime.strptime(notice["date_of_birth"], "%Y/%m/%d")
                item["case_age"] = self.calculate_age(birthdate_object)
            except Exception as e:
                if notice["date_of_birth"]:
                    item["case_age"] = "Birthdate: " + notice["date_of_birth"]
                else:
                    item["case_age"] = "UNKNOWN"

            try:
                item["case_area"] = " - ".join(notice["countries_likely_to_be_visited"]) + " (abbreviations, check link)"
            except Exception as e:
                item["case_area"] = "Check link"
            item["case_country_reported"] = notice["issuing_country"]
            item["case_text"] = "Check link"
            item["case_link"] = self.display_url + "#" + notice["entity_id"].replace("/","-")

            yield item

        return None

    def parse(self, response):

        end_date = datetime.datetime.now()
        #end_date = datetime.datetime(2003, 7, 7) debug 

        while True:
            #https://ws-public.interpol.int/notices/v2/yellow?&dateOfDisapearanceFrom=2024%2F10%2F01&dateOfDisapearanceTo=2024%2F10%2F01
            url_part1 = "?resultPerPage=160&dateOfDisapearanceFrom="
            from_date = (end_date - datetime.timedelta(days=8)).strftime('%Y-%m-%d').replace("-","%2F")
            to_date = end_date.strftime('%Y-%m-%d').replace("-","%2F")

            url_part2 = "&dateOfDisapearanceTo="
            #next_page = https://ws-public.interpol.int/notices/v2/yellow?&dateOfDisapearanceFrom=2024%2F10%2F01&dateOfDisapearanceTo=2024%2F10%2F0
            
            if end_date.year < 1985: # do last range all in one
                start_date = datetime.datetime(1923, 9, 7)
                end_date = datetime.datetime(1985, 9, 7)
                from_date = start_date.strftime('%Y-%m-%d').replace("-","%2F")
                to_date = end_date.strftime('%Y-%m-%d').replace("-","%2F")
                next_page = self.core_api_url + url_part1 + from_date + url_part2 + to_date
                time.sleep(0.1)
                yield scrapy.Request(next_page, callback=self.parse_entries)
                break # Stop, every available case is parsed
            else: # iterate per day
                next_page = self.core_api_url + url_part1 + from_date + url_part2 + to_date
            
            time.sleep(0.1)
            yield scrapy.Request(next_page, callback=self.parse_entries)
            end_date -= datetime.timedelta(days=8)
            
