import scrapy
import json
from selenium.webdriver.common.by import By
from WebScraping.selenium import SeleniumBase
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
class RoehamptonSpider(scrapy.Spider):
    name = 'roe'
    file_name = 'University of Roehamption 2025'
    start_urls = [
        'https://www.roehampton.ac.uk/study/undergraduate-courses/?page=10',
        'https://www.roehampton.ac.uk/study/postgraduate-taught-courses/?page=8',
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
        self.selenium.get_page_urls(response.url)
        course_name = response.xpath('(//div[contains(@class,"col-12 col-lg-6")]//article)[1]').get()
        intake = response.xpath('(//div[contains(@class,"row courses-info")]//article)[1]').get()
        international_fee = response.xpath('(//p[contains(.,"international tuition fees")]//following-sibling::p[contains(text(),"£")]/text())[1]').get()
        if not international_fee:
            international_fee = response.xpath('//h4[contains(text(),"international")]//following-sibling::div/table//td[contains(text(),"£")]').get()
        
        structure_xpath = '//section[contains(@class,"editorial")]//div//label'
        course_structure = self.selenium.getting_target_elements(By.XPATH, structure_xpath)

        self.logger.info(f"""
            ----------------------------------------------------------------------
                         course_structure:{course_structure}
            ----------------------------------------------------------------------
            """)



        carrer = response.xpath(
            '//h2[contains(.,"Career")]//following-sibling::div//ul'
        ).get()
        duration = response.xpath('//p[contains(.,"Duration")]//following-sibling::p/text()').get()
        loader = ItemLoader(item=WebscrapingItem(), response=response)


        if not duration:
            duration = response.xpath('//h2[contains(text(),"Modules")]//following-sibling::div').get()

        if international_fee:
            loader.add_value("Fee_Year", '2025')
            loader.add_value("Fee_Term", 'Year')
            loader.add_value("Currency", 'GBP')


        loader.add_value("Course_Website", response.url)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Intake_Month", intake)
        loader.add_value("International_Fee", international_fee)
        loader.add_value("Career", carrer)
        loader.add_value("Duration", duration)
        loader.add_value("Course_Structure", course_structure)
        loader.add_value("Duration_Term", duration)
        loader.add_value("Study_Load", duration)

        yield loader.load_item()
        
        
