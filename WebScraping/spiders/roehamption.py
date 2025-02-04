import scrapy
import json
from selenium.webdriver.common.by import By
from WebScraping.selenium import SeleniumBase
class RoehamptonSpider(scrapy.Spider):
    name = 'roe'
    file_name = 'University of Roehamption 2025'
    start_urls = [
        'https://www.roehampton.ac.uk/study/undergraduate-courses/',
        'https://www.roehampton.ac.uk/study/postgraduate-taught-courses/',
        'https://www.roehampton.ac.uk/study/higher-technicals/'
    ]
    def __init__(self, *args, **kwargs):
        super(RoehamptonSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()

    def parse(self, response):
        self.selenium.get_page_urls(response.url)        

        course_xpath = '//div[contains(@class,"teaser--course")]//a'
        courses = self.selenium.get_element_urls(By.XPATH, course_xpath) 
        self.logger.info(f"Total Courses: {courses}:Course Length:{len(courses)}")
        for course in courses:
            if course:
                yield scrapy.Request(course, callback=self.parse_course)
    
    def parse_course(self, response):
        course_name = response.xpath('(//div[contains(@class,"col-12 col-lg-6")]//article)[1]').get()
        intake = response.xpath('(//div[contains(@class,"row courses-info")]//article)[1]').get()
        international_fee = response.xpath('(//p[contains(.,"international tuition fees")]//following-sibling::p[contains(text(),"£")]/text())[1]').get()
        carrer = response.xpath(
            '//h2[contains(.,"Career")]//following-sibling::div//ul'
        ).get()

        if international_fee:
            year = "2025"
            term = "Year"
            currency = "GBP"
        
