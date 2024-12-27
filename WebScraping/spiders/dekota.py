import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem


class DekotaSpider(scrapy.Spider):
    name = 'kota'
    file_name = 'Dekota State Univeristy 2025'

    start_urls = ['https://dsu.edu/academics/majors-degrees.html']


    def parse(self, response, **kwargs):
        courses = response.xpath('//a[contains(@class,"results__link")]/@href').getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        title = response.xpath('//h1[contains(@class,"hero__title")]').get()
        intake = response.xpath('//h3[contains(text(),"Start Terms")]/parent::div').get()
        carrer = response.xpath('//h2[contains(text(),"Career possibilities")]/parent::div//following-sibling::div//ul').get()
        study_mode = response.xpath('//h3[contains(text(),"Available")]/parent::div').get()
        course_des = response.xpath('(//div[contains(@class,"main__content")])[1]').get()

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value('Course_Website', response.url)
        loader.add_value('Intake_Month', intake)
        loader.add_value('Course_Name', title)
        loader.add_value('Career', carrer)
        loader.add_value('Study_mode', study_mode)
        loader.add_value('Course_Description', course_des)

        yield loader.load_item()
