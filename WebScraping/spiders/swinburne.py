import scrapy
import pandas as pd
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader
from WebScraping.excel_merger import ExcelFileMerger

class SwinSpider(scrapy.Spider):
    name = 'swin'
    file_name = 'Swinburne University 2025 data'

    def start_requests(self):
        df = pd.read_excel('/home/stone/Downloads/Swinburne University of Technology - 2024.xlsx')

        for url in df['Course Website']:
            if url:
                yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response, **kwargs):

        inter_fee = response.xpath('(//div[contains(@class,"col-sm-6 col-md-2 course-fees__block international")]//p)[1]').get()
        cw = response.url

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None


        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", cw)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)

        yield loader.load_item()
