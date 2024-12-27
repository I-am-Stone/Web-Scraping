import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem


class WrightSpider(scrapy.Spider):
    name = 'wright'
    file_name = 'Wright State University'

    start_urls = ['https://www.wright.edu/degrees-and-programs']

    def parse(self, response):
        courses = response.xpath('//div[contains(@class,"item-list")]//a/@href').getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        print('Course_urls:',response.url)

        course_web_url = response.xpath('//li[contains(@class,"department")]/a/@href').get()
        if course_web_url:
            yield response.follow(course_web_url, callback=self.parse_courses)
    
    def parse_courses(self, response):
        title = response.xpath('//h1[contains(@id,"page-title")]').get()
        course_des = response.xpath('(//h2[contains(text(),"Why")]//following-sibling::p)[position() < 3]').getall()
        carrer= response.xpath('//h4[contains(text(),"work as")]//following-sibling::ul').get()

        print('Program_urls::',response.url)
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value('Course_Website', response.url)
        loader.add_value('Course_Name',title )
        loader.add_value('Course_Description',course_des)
        loader.add_value('Career', carrer)

        yield loader.load_item()

