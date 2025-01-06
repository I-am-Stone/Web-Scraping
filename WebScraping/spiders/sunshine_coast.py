import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem


class CoastSpider(scrapy.Spider):
    name = "coast"
    file_name = "Univeristy of the sunshine Coast Australia 2025"

    def start_requests(self):
        df = pd.read_excel(
            "/home/stone/Downloads/University of the Sunshine Coast - 2024.xlsx"
        )

        for url in df["Course Website"]:
            if url:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        inter_fee = response.xpath(
            '(//div[contains(@audience, "international")]//strong[contains(@class,"key-figure")])[3]'
        ).get()
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("International_Fee", inter_fee)
        print(response.url)

        yield loader.load_item()
