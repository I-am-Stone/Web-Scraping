import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from typing import Any, Dict
import re

def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass


class WestminsteSpider(scrapy.Spider):
    name = "min"
    file_name = "University of Westminste 2025"
    # start_urls = ["https://www.westminster.ac.uk/course-search"]


    def start_requests(self):
        base_url = 'https://www.westminster.ac.uk/course-search?page={}'

        for page in range(1, 57):
            url = base_url.format(page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        courses = response.xpath(
            '//div[contains(@class,"view-content")]//a/@href'
        ).getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)

        self.logger.info(f"Total Courses: {len(courses)}")

        next_page = response.xpath('//ul[contains(@class,"pagination")]//li/a').getall()
        for page in next_page:
            if page:
                yield response.follow(page, callback=self.parse)

    def parse1(self, response):
        title = response.xpath('//section[contains(@class,"masthead-course__header")]//h1').get()
        course_des = response.xpath(
            '//h2[contains(text(),"Course summary")]/parent::div'
        ).get()
        carrer = response.xpath(
            '//h3[contains(text(),"Job roles")]//following-sibling::ul'
        ).get()

        course_struct = response.xpath(
            '//h2[contains(text(),"Course structure")]//parent::div//ul'
        ).getall()

        duration = response.xpath(
            '//span[contains(text(),"Duration")]//following-sibling::span/text()'
        ).get()
        city = response.xpath(
            '//span[contains(text(),"Campus")]//following-sibling::span/a/text()'
        ).get()

        int_fee = response.xpath('//span[contains(text(),"International")]//following-sibling::span/a/text()').get()

        intake = response.xpath('//button[contains(@aria-labelledby,"attendanceSelector")]/text()').get()
        ietls = response.xpath('//li[contains(text(),"IELTS")]').get()
        if not ietls:
            ietls = response.xpath('//p[contains(text(),"IELTS")]//text()').get()
        ietls = ielts_processor(ietls)

        print("Program_urls::", response.url)
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("Course_Name", title)
        loader.add_value("Course_Description", course_des)
        loader.add_value("Career", carrer)
        loader.add_value("Course_Structure", course_struct)
        loader.add_value("Duration", duration)
        loader.add_value("Duration_Term", duration)
        loader.add_value("City",city)
        loader.add_value("International_Fee",int_fee)
        loader.add_value("Degree_level", title)
        loader.add_value("Intake_Month", intake)
        loader.add_value("Study_Load", intake)

    
        if ietls:
            loader.add_value('IELTS_Overall', ietls[0])
            loader.add_value('IELTS_Reading', ietls[1])
            loader.add_value('IELTS_Writing', ietls[1])
            loader.add_value('IELTS_Listening', ietls[1])
            loader.add_value('IELTS_Speaking', ietls[1])


        if int_fee:
            loader.add_value("Fee_Year", '2025')
            loader.add_value("Fee_Term", 'Year')
            loader.add_value("Currency", 'GBP')




        yield loader.load_item()