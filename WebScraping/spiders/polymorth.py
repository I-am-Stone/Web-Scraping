import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
import re 
from typing import Dict, Any
import json
from scrapy.selector import Selector

def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          value.replace('C/4', '')
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass
    
class PlymouthSpider(scrapy.Spider):
    name = 'ply'
    file_name = 'University of Plymouth'
    start_urls = ['https://www.plymouth.ac.uk/courses/search.json?page=5&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Engineering%2C%20Computing%20and%20Mathematics',
                  'https://www.plymouth.ac.uk/courses/search.json?page=2&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=Plymouth%20Business%20School',
                  'https://www.plymouth.ac.uk/courses/search.json?page=3&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Art%2C%20Design%20and%20Architecture',
                  'https://www.plymouth.ac.uk/courses/search.json?page=4&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Biological%20and%20Marine%20Sciences',
                  'https://www.plymouth.ac.uk/courses/search.json?page=5&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Engineering%2C%20Computing%20and%20Mathematics',
                  'https://www.plymouth.ac.uk/courses/search.json?page=6&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Geography%2C%20Earth%20and%20Environmental%20Sciences',
                  'https://www.plymouth.ac.uk/courses/search.json?page=7&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Nursing%20and%20Midwifery',
                  'https://www.plymouth.ac.uk/courses/search.json?page=8&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Psychology',
                  'https://www.plymouth.ac.uk/courses/search.json?page=9&ug=true&pgt=true&pgr=true&cpd=true&uop=true&q=&dynamic=true&previous=School%20of%20Society%20and%20Culture']


    def parse(self, response):
        data = json.loads(response.text)
        results = data['html']
        
        selector = Selector(text=results)
        
        # Now apply XPath to the selector
        courses = selector.xpath('//li/a/@href').getall()
        
        self.logger.info(f"Total Courses: {len(courses)}")
        self.logger.info(f"Course urls: {courses}")

        for course in courses:
            if course:
                urls = 'https://www.plymouth.ac.uk' + course
                yield scrapy.Request(urls, callback=self.parse1)
    
    def parse1(self, response):
        self.logger.info(f"Course url: {response.url}")
        course_name = response.xpath('//h1[contains(@class,"course-clearing-title")]//text()').get()
        duration = response.xpath('//td[contains(text(),"Duration")]//following-sibling::td/p/text()').get()
        study_load = response.xpath('//td[contains(text(),"Course type")]//following-sibling::td/p/text()').get()
        city = response.xpath('//td[contains(text(),"Study location")]//following-sibling::td/text()').get()
        course_des = response.xpath('//div[contains(@class,"overview")]').get()
        course_structure = response.xpath('//span[contains(@class,"course-info")]/strong').get()
        ielts = response.xpath('//strong[contains(text(),"IELTS")]//following-sibling::text()').get()
        if not ielts:
            ielts = response.xpath('//li[contains(text(),"IELTS")]//text()').get()
        inter_fees = response.xpath('(//td[contains(.,"International")]//following-sibling::td)[2]').get()
        ielts = ielts_processor(ielts)

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Duration", duration)
        loader.add_value("Study_Load", study_load)
        loader.add_value("City", city)
        loader.add_value("Course_Description", course_des)
        loader.add_value('Course_Structure', course_structure)
        loader.add_value("International_Fee", inter_fees)

        if ielts:
            loader.add_value('IELTS_Overall', ielts[0])
            loader.add_value('IELTS_Reading', ielts[0])
            loader.add_value('IELTS_Writing', ielts[0])
            loader.add_value('IELTS_Listening', ielts[0])
            loader.add_value('IELTS_Speaking', ielts[0])
        if inter_fees:
            loader.add_value("Fee_Year",'2025')
            loader.add_value("Fee_Term", 'Year')
            loader.add_value("Currency", 'AUD')
        
        yield loader.load_item()
