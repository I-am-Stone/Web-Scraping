import scrapy
import json
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
    allowed_domains = ["tafe.nsw.edu.au"]
    start_urls = ["https://www.tafensw.edu.au/international/course-search?keyword="]

    def __init__(self, *args, **kwargs):
        super(TafeSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()

    def parse(self, response):
        self.selenium.get_page_urls(response.url)

        course_xpath = '//a[contains(@class,"group")]'
        courses = self.selenium.get_element_urls(By.XPATH, course_xpath) 
        # self.logger.info(f"Total Courses: {courses}")
        for course in courses:
            print(course)
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        ielts =  response.xpath('//li[contains(text(),"IELTS")]/text()').get()
        ielts = ielts_processor(ielts)
        print(ielts)

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_xpath("Course_Name", '//h1/text()')
        loader.add_xpath("Course_Description", '//div[contains(@id,"overview-text")]')
        loader.add_xpath("Duration", '//h3[contains(text(),"Duration ")]//following-sibling::div//strong')
        loader.add_xpath("Duration_Term", '//h3[contains(text(),"Duration ")]//following-sibling::div//strong')
        loader.add_xpath("International_Fee",'//h3[contains(text(),"Course fee")]//following-sibling::div//strong')
        loader.add_value('IELTS_Overall', ielts[0])
        loader.add_value('IELTS_Reading', ielts[0])
        loader.add_value('IELTS_Writing', ielts[0])
        loader.add_value('IELTS_Listening', ielts[0])
        loader.add_value('IELTS_Speaking', ielts[0])
        # yield loader.load_item()
