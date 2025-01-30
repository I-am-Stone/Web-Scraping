import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
import json
from typing  import Dict, Any
from WebScraping.selenium import SeleniumBase
from selenium.webdriver.common.by import By

class MelbourneSpider(scrapy.Spider):
    name = "melbourne"
    file_name = 'Melbourne Polytechnic 2025'

    start_urls = ['https://www.melbournepolytechnic.edu.au/search/?studentType=1&query=&activeTab=0&page=1',
                  'https://www.melbournepolytechnic.edu.au/search/?studentType=1&query=&activeTab=0&page=2',
                  'https://www.melbournepolytechnic.edu.au/search/?studentType=1&query=&activeTab=0&page=3',
                  'https://www.melbournepolytechnic.edu.au/search/?studentType=1&query=&activeTab=0&page=4',
                  'https://www.melbournepolytechnic.edu.au/search/?studentType=1&query=&activeTab=0&page=5']
    
    def __init__(self, name = None, **kwargs):
        super(MelbourneSpider, self).__init__(name, **kwargs)
        self.selenium = SeleniumBase()

    def parse(self, response):
        self.selenium.get_page_urls(response.url)
        course_xpath = '//div[contains(@class,"mp-search-entry")]//a'
        courses = self.selenium.get_element_urls(By.XPATH, course_xpath)
        self.logger.info(f"Total Courses: {courses}")
        
        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse_courses)


    def parse_courses(self, response):
        self.logger.info(f"Total Courses: {response.url}")

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        yield loader.load_item()
