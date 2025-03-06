import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from typing import Dict, Any
import re

def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          value.replace('C/4', '')
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass

class ChisterSpider(scrapy.Spider):
    name = 'chi'
    file_name = "Chister Univeristy 2025"

    def start_requests(self):
        url_base = 'https://www.chi.ac.uk/courses/?_sft_learning_level=undergraduate%2Cpostgraduate&sf_paged={}'

        for page in range(1, 22):
            url = url_base.format(page)
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        courses = response.xpath('//div[contains(@class,"course-title")]//a/@href').getall()

        self.logger.info(f"Parsing course: {len(courses)}")


        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        self.logger.info("Parsing course: %s" % response.url)
        course_name = response.xpath(
            '//h1[contains(@class,"fl-heading")]//span/text()'
        ).get()
        duration = response.xpath(
            '//div[contains(@class,"course-length-wrap")]/span/text()'
        ).get()
        course_description = response.xpath(
            '//h2[contains(text(),"Overview")]/parent::div//following-sibling::div'
        ).get()
        carrer =response.xpath('//h2[contains(text(),"Careers")]//parent::div//following-sibling::div//ul').get()

        inter_fee = response.xpath(
            '//h5[contains(text(),"International fee")]//parent::div//following-sibling::div/div/text()'
        ).get()

        city = response.xpath('//div[contains(@class,"course-campus-wrap")]/span/text()').get()

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "GBP" if inter_fee else None
        ielts_overall = response.xpath('//h5[contains(text(),"IELTS")]/parent::div//following-sibling::div/div/text()').get()

        item = ItemLoader(item=WebscrapingItem(), response=response)
        item.add_value('Course_Website', response.url)
        item.add_value('Course_Name', course_name)
        item.add_value('Duration', duration)
        item.add_value('Course_Description', course_description)
        item.add_value('Duration_Term', duration)
        item.add_value('Study_Load', duration)
        item.add_value('Career', carrer)
        item.add_value('International_Fee', inter_fee)
        item.add_value('Fee_Year', year)
        item.add_value('Fee_Term', term)
        item.add_value('Currency', currency)
        item.add_value('City', city)

        ielts = response.xpath('//h5[contains(text(),"IELTS")]/parent::div//following-sibling::div/following-sibling::div/text()').get()
        ielts = ielts_processor(ielts)
        if ielts_overall:
            item.add_value('IELTS_Overall', ielts_overall)

        if ielts:
            item.add_value('IELTS_Reading', ielts[0])
            item.add_value('IELTS_Writing', ielts[0])
            item.add_value('IELTS_Listening', ielts[0])
            item.add_value('IELTS_Speaking', ielts[0])
        
        return item.load_item()
