import scrapy
import json
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader

class lsbuSpider(scrapy.Spider):
    name = 'lsbu'
    file_name = 'london South Bank  University 2025'
    
    start_urls = ['https://lsbu-search.clients.uk.funnelback.com/s/search.json?collection=LSBU_Courses_Meta&num_ranks=131&start_rank=1&query=!nullsearch&f.Level_new|courseLevel=undergraduate&sort=relevance&profile=_default',
                  'https://lsbu-search.clients.uk.funnelback.com/s/search.json?collection=LSBU_Courses_Meta&num_ranks=77&start_rank=1&query=!nullsearch&f.Level_new|courseLevel=postgraduate&sort=relevance&profile=_default']
    
    def parse(self, response):
        data = json.loads(response.text)
        results = data['response']['resultPacket']['results']
        course_urls = []
        for result in results:
            url = result.get('liveUrl',None)
            course_urls.append(url)

        
        
        self.logger.info(f"Total Courses: {len(course_urls)}")
        self.logger.info(f"Course urls: {course_urls}")
        for url in course_urls:
            if url:
                yield scrapy.Request(url, callback=self.parse_course)
    
    def parse_course(self, response):
        course_name = response.xpath('//h1[contains(@class,"top-banner__main-title")]').get()
        durration = response.xpath('//span[contains(text(),"Duration")]//following-sibling::span').get()
        study_load = response.xpath('//span[contains(text(),"Mode")]//following-sibling::span').get()
        intake = response.xpath('//span[contains(text(),"Start date")]//following-sibling::span').get()
        course_des = response.xpath('//div[contains(@class,"overview-description")]').get()
        international_fees = response.xpath('(//p[contains(@class,"fees__card-subtitle")])[2]').get()
        city = response.xpath('//a[contains(@id,"-campus")]//text()').get()
        course_strcture = response.xpath('//div[contains(@id,"course-content")]//ul').get()

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value('Course_Name',course_name)
        loader.add_value('Duration',durration)
        loader.add_value('Intake_Month',intake)
        loader.add_value('Course_Description',course_des)
        loader.add_value('International_Fee', international_fees)
        loader.add_value('City',city)
        loader.add_value('Course_Structure', course_strcture)
        loader.add_value("Study_Load",study_load)
        loader.add_value("Course_Website", response.url)
        year = "2025" if international_fees else None
        term = "Year" if international_fees else None
        currency = "GBP" if international_fees else None

        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)


        yield loader.load_item()





