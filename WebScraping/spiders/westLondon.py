import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
from typing import Any, Dict
import re
from WebScraping.selenium import SeleniumBase
from selenium.webdriver.common.by import By

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

    def __init__(self, *args, **kwargs):
        super(WestLondonSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()


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
        self.selenium.get_page_urls(response.url)
        self.logger.info(f" Courses Urls : {response.url}")
        course_name = response.xpath('//div[contains(@class,"page-header__title u-relative")]//span/text()').get()
        duration = response.xpath('//div[contains(text(),"Duration:")]/text()').get()
        city = response.xpath('//input[contains(@id,"location")]/@value').get()
        duration_term = response.xpath('//div[contains(text(),"Duration:")]/text()').get()
        
        intake_xpath = '//label[contains(text(),"Start date")]//following-sibling::div/div'
        intake_month = self.selenium.getting_target_element(By.XPATH, intake_xpath)
        
        course_des = response.xpath('//h2[contains(text(), "study")]//parent::div//following-sibling::div').get()
        course_structure = response.xpath('//h3[contains(text(),"Compulsory modules")]//following-sibling::div//li//span').get()

        self.logger.info(f" course_structure : {course_structure}")
        fees_xpath = '//option[contains(text(),"International")]'
        fees = self.selenium.getting_target_element(By.XPATH, fees_xpath)
        self.logger.info(f" Fees : {fees}")

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Duration", duration)
        loader.add_value("Duration_Term", duration_term)
        loader.add_value("City", city)
        loader.add_value("International_Fee", fees)
        loader.add_value("Intake_Month", intake_month)
        loader.add_value("Course_Structure", course_structure)
        loader.add_value("Course_Description", course_des)
       
        # yield loader.load_item()

        