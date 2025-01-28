import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from typing import Any, Dict
from selenium.webdriver.common.by import By
from WebScraping.selenium import SeleniumBase
import re

def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass


class TafeSpider(scrapy.Spider):
    name = "tafe_nsw"
    file_name = "TAFE NSW 2025"
    start_urls = ["https://www.tafensw.edu.au/international/course-search?keyword="]

    def __init__(self, *args, **kwargs):
        super(TafeSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()

    def parse(self, response):
        self.selenium.get_page_urls(response.url)

        course_xpath = '//a[contains(@class,"group")]'
        courses = self.selenium.get_element_urls(By.XPATH, course_xpath) 
        self.logger.info(f"Total Courses: {courses}")
        for course in courses:
            if course:
                yield scrapy.Request(course, callback=self.parse_course)
    
    def parse_course(self, response):

        print("Course_urls:", response.url)

        ielts =  response.xpath('//li[contains(text(),"IELTS")]/text()').get()
        ielts = ielts_processor(ielts)
        print(ielts)

        city = response.xpath('(//div[contains(@class,"table-overflow intakes-table")]//table)[1]').get()
        intake = response.xpath('(//div[contains(@class,"table-overflow intakes-table")]//table)[1]').get()

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_xpath("Course_Name", '//h1/text()')
        loader.add_xpath("Course_Description", '//div[contains(@id,"overview-text")]')
        loader.add_xpath("Course_Description", '//div[contains(@class,"mt-8 mb-4 md:mb-6 lg:mb-0 text-base")]/p')
        loader.add_xpath("Duration", '//h3[contains(text(),"Duration ")]//following-sibling::div//strong')
        loader.add_xpath("Duration_Term", '//h3[contains(text(),"Duration ")]//following-sibling::div//strong')
        loader.add_xpath("International_Fee",'//h3[contains(text(),"Course fee")]//following-sibling::div//strong')
        loader.add_xpath("International_Fee",'//h3[contains(text(),"Package fee")]//following-sibling::div//strong')
        loader.add_value("City",city)
        loader.add_value("Intake_Month",intake)

        loader.add_value('IELTS_Overall', ielts[0])
        loader.add_value('IELTS_Reading', ielts[0])
        loader.add_value('IELTS_Writing', ielts[0])
        loader.add_value('IELTS_Listening', ielts[0])
        loader.add_value('IELTS_Speaking', ielts[0])
        loader.add_value("Fee_Year",'2025')
        loader.add_value("Fee_Term", 'Year')
        loader.add_value("Currency", 'AUD')
        yield loader.load_item()
