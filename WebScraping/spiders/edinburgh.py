import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
from typing import Any, Dict
import re
def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass

class WestLondonSpider(scrapy.Spider):
    name = 'west'
    file_name = 'University of West London 2025'
    start_urls = ['https://www.uwl.ac.uk/courses/search?query=&f%5B0%5D=course_type%3Acourse']
    custom_settings = {
    'DEFAULT_REQUEST_HEADERS': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
}


    def parse(self, response):
        courses = response.xpath('//div[contains(@class,"views-row")]//a[contains(@class,"link u-no-underline")]/@href').getall()

        self.logger.info(f"Total Courses: {len(courses)}")
        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)

        next_page = response.xpath('//li[contains(@class,"page-item")]//a/@href').getall()
        for page in next_page:
            if page:
                response.follow(page, callback=self.parse)
    
    def parse1(self, response):
        self.logger.info(f" Courses Urls : {response.url}")
        course_name = response.xpath('//div[contains(@class,"page-header__title u-relative")]//span/text()').get()
        duration = response.xpath('//div[contains(text(),"Duration:")]/text()').get()
        city = response.xpath('//input[contains(@id,"location")]/@value').get()
        duration_term = response.xpath('//div[contains(text(),"Duration:")]/text()').get()
        fees = response.xpath('//option[contains(text(),"International")]').get()
        
        study_load = response.xpath('//span[contains(text(),"Delivery")]//following-sibling::text()').get()
        course_des = response.xpath('//div[contains(@id,"introduction")]').get()
        course_structure = response.xpath('//div[contains(@id,"collapseWhatStudy")]//h3 | //div[contains(@id,"collapseWhatStudy")]//ul').getall()
        carrer = response.xpath('//p[contains(text(),"employed")]//following-sibling::ul').get()
        self.logger.info(f"""---------------------------------
                         Course Structure: {course_structure}
                         ---------------------------------""")
        ielts = response.xpath('(//li[contains(.,"IELTS")]//text())[2]').get()
        tofel = response.xpath('(//li[contains(.,"TOEFL-iBT")]//text())[2]').get()
        pte = response.xpath('(//li[contains(.,"PTE")]//text())[2]').get()

        ielts = ielts_processor(ielts)
        tofel = ielts_processor(tofel)
        pte = ielts_processor(pte)

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Duration", duration)
        loader.add_value("Duration_Term", duration_term)
        loader.add_value("Study_Load", study_load)
        loader.add_value("Course_Description", course_des)
        loader.add_value("Course_Structure", course_structure)
        loader.add_value("Career", carrer)
        loader.add_value("City", city)

        loader.add_value('IELTS_Overall', ielts[0])
        loader.add_value('IELTS_Reading', ielts[1])
        loader.add_value('IELTS_Writing', ielts[1])
        loader.add_value('IELTS_Listening', ielts[1])
        loader.add_value('IELTS_Speaking', ielts[1])

        loader.add_value('TOEFL_Overall', tofel[0])
        loader.add_value('TOEFL_Reading', tofel[1])
        loader.add_value('TOEFL_Writing', tofel[1])
        loader.add_value('TOEFL_Listening', tofel[1])
        loader.add_value('TOEFL_Speaking', tofel[1])

        loader.add_value('PTE_Overall', pte[0])
        loader.add_value('PTE_Reading', pte[1])
        loader.add_value('PTE_Writing', pte[1])
        loader.add_value('PTE_Listening', pte[1])
        loader.add_value('PTE_Speaking', pte[1])

        # yield loader.load_item()

        