import scrapy
from typing import Any
import json
from WebScraping.selenium import SeleniumBase
from typing import Dict, Iterator, Union
from scrapy.http import Response, Request
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from selenium.webdriver.common.by import By
import re

def ielts_processor(value: str) -> Dict[str, Any]:
    try:
          values = re.findall(r'\d+\.*\d*', value)
          return values
    except:
         pass
    
class StirlingSpider(scrapy.Spider):
    name = "stirling"
    file_name: str = "University of Stirling 2025"
    start_urls:list[str] = ["https://search.stir.ac.uk/s/search.json?collection=stir-courses&SF=[c%2Caward%2Ccode%2Cdelivery%2Cfaculty%2Cimage%2Clevel%2Cmodes%2Cpathways%2Csid%2Cstart%2Csubject%2Cucas]&fmo=true&num_ranks=211&explain=true&query=!padrenullquery&timestamp=1738307447098&start_rank=1&curator=true&sort=title"]

    def __init__(self, name = None, **kwargs):
        super(StirlingSpider, self).__init__(name, **kwargs)
        self.selenium = SeleniumBase()
    
    def parse(self, response:Response) -> Iterator[Union[Dict[str,str]]]:
        course_urls = []
        meta_datas = []
        data: Dict[str, Any] = json.loads(response.text)
        response_parse = data.get('response',{})
        results = response_parse.get('resultPacket',{}).get('results',{})

        if results:
            for item in results:
                if isinstance(item,dict):
                    live_url = item.get('liveUrl')
                    if live_url:
                        course_urls.append(live_url)
                    meta_data = item.get('metaData')
                    intake_month = meta_data.get('start')
                    self.logger.info(f"Intake month: {intake_month}")
                    level = meta_data.get('level')
                    delivery = meta_data.get('delivery')
                    modes = meta_data.get('modes')
                    meta_datas.append(intake_month)
                    meta_datas.append(level)
                    meta_datas.append(delivery)
                    meta_datas.append(modes)
        
        self.logger.info(f"Metadata: {meta_datas}")

        for urls in course_urls:
            if urls:
                yield response.follow(urls, callback=self.parse_course, meta={'intake_month':meta_datas[0], 'level':meta_datas[1], 'delivery':meta_datas[2], 'modes':meta_datas[3]})

    def parse_course(self, response:Response):
        self.selenium.get_page_urls(response.url)
        print(response.url)

        fee_xpath = "(//tr[contains(@data-region,'int-eu')]//td)[2]"
        international_fee = self.selenium.getting_target_element(By.XPATH, fee_xpath)
        
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_xpath("Course_Name","//h1[contains(@class,'course-heading')]/text()")
        loader.add_xpath("Course_Description","//h2[contains(text(),'Overview')]//following-sibling::div")
        loader.add_value("Intake_Month", response.meta['intake_month'])
        loader.add_xpath("Duration",'//strong[contains(text(),"Duration")]//following-sibling::text()')
        loader.add_xpath("Duration_Term",'//strong[contains(text(),"Duration")]//following-sibling::text()')
        ielts = response.xpath('//li[contains(text(),"IELTS")]/text()').get()
        ielts = ielts_processor(ielts)
        if ielts:
            loader.add_value('IELTS_Overall', ielts[0])
            loader.add_value('IELTS_Reading', ielts[1])
            loader.add_value('IELTS_Writing', ielts[1])
            loader.add_value('IELTS_Listening', ielts[1])
            loader.add_value('IELTS_Speaking', ielts[1])

        pte = response.xpath('//li[contains(text(),"Pearson")]/text()').get()
        pte = ielts_processor(pte)
        if pte:
            loader.add_value('PTE_Overall', pte[0])
            loader.add_value('PTE_Reading', pte[1])
            loader.add_value('PTE_Writing', pte[1])
            loader.add_value('PTE_Listening', pte[1])
            loader.add_value('PTE_Speaking', pte[1])

        tofel = response.xpath('//li[contains(text(),"TOEFL")]/text()').get()
        tofel = ielts_processor(tofel)

        if tofel:
            loader.add_value('TOEFL_Overall', tofel[0])
            loader.add_value('TOEFL_Reading', tofel[2])
            loader.add_value('TOEFL_Writing', tofel[1])
            loader.add_value('TOEFL_Listening', tofel[4])
            loader.add_value('TOEFL_Speaking', tofel[3])

        if international_fee:
            loader.add_value("International_Fee",international_fee)
            loader.add_value("Fee_Year", '2025')
            loader.add_value("Fee_Term", 'Year')   
            loader.add_value("Currency", 'AUD')

        loader.add_value("Degree_level", response.meta['level'])
        loader.add_value("Study_mode", response.meta['delivery'])
        loader.add_value("Study_Load", response.meta['modes'])
        yield loader.load_item()
