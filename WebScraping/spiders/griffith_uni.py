import scrapy
import pandas as pd

from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
from selenium.webdriver.common.by import By
from WebScraping.selenium import SeleniumBase


class GriffithSpider(scrapy.Spider):
    name = "fith"
    file_name = "Griffith Univeristy 2025"

    def __init__(self, *args, **kwargs):
        super(GriffithSpider, self).__init__(*args, **kwargs)
        self.selenium = SeleniumBase()

    def start_requests(self):
        df = pd.read_excel(
            "/home/stone/Downloads/Griffith University update23 AUS (2024).xlsx"
        )

        for url in df["Course Website"]:
            if url:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.selenium.get_page_urls(response.url)
        fee_xpath = '//dt[contains(text(),"Fee ")]//following-sibling::div/dd'
        inter_fee = self.selenium.getting_target_element(By.XPATH, fee_xpath)

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None
        loader = ItemLoader(item=WebscrapingItem(), response=response)

        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Course_Website", response.url)

        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)
        yield loader.load_item()
