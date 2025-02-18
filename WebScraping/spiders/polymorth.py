import scrapy

class PlymouthSpider(scrapy.Spider):
    name = 'ply'
    file_name = 'University of Plymouth'
    start_urls = ['https://www.plymouth.ac.uk/subjects']


    def parse(self, response):
        subjects = response.xpath('//div[contains(@class,"gallery-web-refresh-grid-item-3")]//a/@href').get()

        for subject in subjects:
            if subject:
                yield response.follow(subject, callback=self.course_parse)
    
    def course_parse(self, response):
        courses = response.xpath('//ul[contains(@class,"res-courses")]//a/@href').getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)
    
    def parse1(self, response):
        course_name = response.xpath('//h1[contains(@class,"course-clearing-title")]//text()vv').get()
        duration = response.xpath('//td[contains(text(),"Duration")]//following-sibling::td/p/text()').get()
        study_load = response.xpath('//td[contains(text(),"Course type")]//following-sibling::td/p/text()').get()
        city = response.xpath('//td[contains(text(),"Study location")]//following-sibling::td/text()').get()
        course_des = response.xpath('//div[contains(@class,"overview")]').get()
        course_structure = response.xpath('//span[contains(@class,"course-info")]/strong').get()
        ielts = response.xpath('//strong[contains(text(),"IELTS")]//following-sibling::text()').get()
        inter_fees = response.xpath('(//td[contains(.,"International")]//following-sibling::td)[2]').get()
        