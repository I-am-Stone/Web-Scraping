import scrapy
import pandas as pd
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader


class LetHimCook(scrapy.Spider):
    name = "cook"
    file_name = "James Cook Univeristy 2025"

    def start_requests(self):
        df = pd.read_excel("/home/stone/Downloads/James Cook University.xlsx")

        for url in df["Course Website"]:
            if url:
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",  # Custom header for Scrapy requests
                    },
                )

    def parse(self, response):
        inter_fee = response.xpath('(//p[contains(text(),"$")])[1]/text()').get()
        cw = response.url
        intake = response.xpath(
            '//li[contains(@class,"course-fast-facts__location")]//strong'
        ).getall()
        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None

        print(intake)

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", cw)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Intake_Month", intake)
        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)

        yield loader.load_item()
