import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem


class MurdochSpider(scrapy.Spider):
    name = "chod"
    file_name = "MUrdoch Univeristy 2025"

    def start_requests(self):
        df = pd.read_excel(
            "/home/stone/Downloads/2024_03_05_16_20_01_Murdoch_University_new_2024_1.xlsx"
        )

        for url in df["Course Website"]:
            if url:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        inter_fee = response.xpath(
            '(//dt[contains(text(),"First year fee")]//following-sibling::dd)[2]'
        ).get()

        print(response.url)
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("International_Fee", inter_fee)

        yield loader.load_item()
