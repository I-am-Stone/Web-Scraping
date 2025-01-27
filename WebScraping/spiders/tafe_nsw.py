import scrapy
import json
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from typing import Any, Dict
from selenium.webdriver.common.by import By
from WebScraping.selenium import SeleniumBase

class TafeSpider(scrapy.Spider):
    name = "tafe_nsw"
    allowed_domains = ["tafe.nsw.edu.au"]
    start_urls = ["https://www.tafensw.edu.au/international/course-search?keyword="]

    def __init__(self, *args, **kwargs):
        super(TafeSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()

    def parse(self, response):
        self.selenium.get_page_urls(response.url)

        courses = '//a[contains(@class,"group")]'
        courses = self.selenium.get_element_urls(By.XPATH, courses) 
        self.logger.info(f"Total Courses: {len(courses)}")
        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1) 
        