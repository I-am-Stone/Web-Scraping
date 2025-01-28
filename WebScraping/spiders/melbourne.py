import scrapy
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader


class MelbourneSpider(scrapy.Spider):
    name = "melbourne"
    file_name = 'Melbourne Polytechnic 2025'
    start_urls = ["https://www.melbournepolytechnic.edu.au/all-courses/"]

    def parse(self, response):
        courses = response.xpath('//div[contains(@class,"course-list__inner  container__col")]//a/@href').getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)