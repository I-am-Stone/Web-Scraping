import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem

class TechSpider(scrapy.Spider):
    name = 'tech'
    file_name = 'University of technology sydney'

    def start_requests(self):
        df = pd.read_excel('/home/stone/Downloads/University of Technology Sydney (UTS) - 2024(1).xlsx')
        for url in df['Course Website']:
            print(url)
            if url:
                yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        course_fee = response.xpath('//text()[contains(.,"cost per credit")]').get()

        duration = response.xpath('(//h3[contains(text(), "Duration")]//following-sibling::p/text())[1]').get()
        if duration and course_fee:
            course_fee = f"{course_fee} ({duration})"

        print(course_fee)
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value('Course_Website', response.url)
        loader.add_value('International_Fee', course_fee)
        

        yield loader.load_item()
