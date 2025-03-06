import scrapy
from WebScraping.selenium import SeleniumBase
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from selenium.webdriver.common.by import By

class PortSouthSpider(scrapy.Spider):
    name = 'portsouth'
    file_name = 'University of PortSouth 2025'
    
    def __init__(self, name=None, **kwargs):
        super(PortSouthSpider, self).__init__(name, **kwargs)
        self.selenium = SeleniumBase()
    
    def start_requests(self):
        base_url = 'https://www.port.ac.uk/study/courses?page={}&level=Master%E2%80%99s_and_Postgraduate_Taught+Undergraduate'
        for i in range(1, 22):
            url = base_url.format(i)
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        self.selenium.get_page_urls(response.url)
        course_xpath = '//a[contains(@class,"button--overlay")]'
        courses = self.selenium.get_element_urls(By.XPATH, course_xpath)
        self.logger.info(f"-----------------------------------------")
        self.logger.info(f"courses_link: {len(courses)}")
        self.logger.info(f"-----------------------------------------")
        self.logger.info(f"courses_link: {courses}")

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        course_name = response.xpath('//h1[contains(@class,"heading heading--title")]/text()').get()
        course_des = response.xpath('//div[contains(@class,"text-highlighted__content")]').get()
        if not course_des:
            course_des = response.xpath('(//div[contains(@class,"text-highlighted__content")])[4]').get()
        inter_fee = response.xpath('(//strong[contains(text(),"Full-time")]/following-sibling::text())[3]').get()
        if not inter_fee:
            inter_fee = response.xpath('//strong[contains(text(),"International")]/following-sibling::text()').get()
        duration = response.xpath('//input[contains(@name,"course-duration")]//following-sibling::label/text()').get()
        intake_month = response.xpath('//input[contains(@name,"course-start-date")]//following-sibling::label/text()').get()
        loader = ItemLoader(item=WebscrapingItem(), response=response)

        if inter_fee:
            loader.add_value("Fee_Year", '2025')
            loader.add_value("Fee_Term", 'Year')
            loader.add_value("Currency", 'GBP')

        loader.add_value("Course_Name", course_name)
        loader.add_value("Course_Description", course_des)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Intake_Month", intake_month)
        loader.add_value("Course_Website", response.url)
        loader.add_value("Duration", duration)
        loader.add_value("Duration_Term",duration)
        loader.add_value("Study_Load", duration)
        yield loader.load_item()
