import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem


class EngSpider(scrapy.Spider):
    name = "eng"
    file_name = "Univeristy of New england 2025"

    start_urls = ["https://www.une.edu.au/study/courses"]
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }

    def parse(self, response):
        courses = response.xpath(
            '//div[contains(@class,"tiles__item")]//a/@href'
        ).getall()
        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)

    def parse1(self, response):
        print(response.url)

    def parse2(self, response):
        print(response.url)

        cn = response.xpath('//h1[contains(@class,"banner__title")]').get()
        fees = response.xpath(
            '//td[contains(text(),"International")]//following-sibling::td'
        ).get()
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        loader.add_value("International_Fee", fees)
        loader.add_value("Course_Name", cn)

        yield loader.load_item()
