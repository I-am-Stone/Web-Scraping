import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)
from scrapy.http import Response


class BondSpider(scrapy.Spider):
    name = "bon"
    file_name = "Bond University 2025"

    def start_requests(self):
        df = pd.read_excel(
            "/home/stone/Downloads/2024_02_09_16_38_40_Bond_University_1.xlsx"
        )

        for url in df["Course Website"]:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: Response):
        fees_url = response.xpath('//a[contains(text(),"Fees")]/@href')
        cw = response.url

        meta = [cw]

        for url in fees_url:
            if url:
                yield response.follow(
                    url, callback=self.parse_course, meta={"meta": meta}
                )

    def parse_course(self, response: Response):
        meta = response.meta["meta"]
        print(meta[0])
        course_fee = response.xpath('(//span[contains(@class,"program-fee")])[1]').get()

        print(course_fee)

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", meta[0])
        loader.add_value("International_Fee", course_fee)

        yield loader.load_item()
