from typing import Any, Dict, List, Optional, Iterator, Union
import scrapy
from scrapy.http import Response, Request
import json
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader

def ietls_check(value) -> list[str]:
    certificate = ['6.0','5.5','5.5','5.5','5.5']
    bachelor = ['6.0','6.0','6.0','6.0','6.0']
    nursing = ['7.0','7.0','7.0','7.0','7.0'] #nursing and psychology
    master = ['6.5','6.0','6.0','6.0','6.0'] # master exercise and sports, law

def tofel_check(value) -> list[str]:
    certificate = ['64','8','7','16','18'] # o index overall, 1 reading, 2 listing, 3 speaking, 4 writing
    bachelor = ['64','13','12','18','21']
    nursing = ['94','24','24','23','27'] #nursing and psychology
    master = ['79','','6.0','6.0','6.0']

def pte_check(value) -> list[str]:
    certificate = ['6.0','5.5','5.5','5.5','5.5']
    bachelor = ['6.0','6.0','6.0','6.0','6.0']
    nursing = ['7.0','7.0','7.0','7.0','7.0'] #nursing and psychology ,master Dietetic, master occupational
    master = ['6.5','6.0','6.0','6.0','6.0']


class SwinSpider(scrapy.Spider):
    name: str = 'swin'
    file_name: str = 'Swinburne_University_2025_v2'
    start_urls: List[str] = ['https://search.swinburne.edu.au/s/search.html?collection=swinburne-course-search&query=Master&tierbars=false&num_ranks=759&smeta_AccreditationStatus=current&f.Course+type|CourseTypes=advanced+diploma&f.Course+type|CourseTypes=bachelor+degree&f.Course+type|CourseTypes=bachelor+degree+with+honours&f.Course+type|CourseTypes=bachelor+degree+with+work+placement&f.Course+type|CourseTypes=certificate+i&f.Course+type|CourseTypes=certificate+ii&f.Course+type|CourseTypes=certificate+iii&f.Course+type|CourseTypes=certificate+iv&f.Course+type|CourseTypes=diploma&f.Course+type|CourseTypes=graduate+certificate&f.Course+type|CourseTypes=graduate+diploma&f.Course+type|CourseTypes=honours+degree&f.Course+type|CourseTypes=master%E2%80%99s+degree+by+course+work&f.Course+type|CourseTypes=master%E2%80%99s+degree+by+research']
    
    custom_settings: Dict[str, Any] = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; SwinburneBot/1.0)',
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1.0,
    }

    def parse(self, response: Response) -> Iterator[Union[Dict[str, str], Request]]:
        """
        Parse the JSON response from the search page.
        
        Args:
            response: The response object from the request.
            
        Yields:
            Either a dictionary containing course URLs or Requests for course pages.
        """
        try:
            course_urls = []
            data: Dict[str, Any] = json.loads(response.text)
            resutls = data.get('results',{})
            self.logger.info(f"Course_len {len(resutls), course_urls}")

            for item in resutls:
                if isinstance(item,dict):
                    live_url = item.get('urls',{}).get('liveUrl')
                    if live_url:
                        course_urls.append(live_url)
            self.logger.info(f"Course_len {len(course_urls), course_urls}")

            for urls in course_urls:
                if urls:
                    yield response.follow(urls, callback=self.parse_course)
        except Exception as e:
            self.logger.error(f"Error processing response: {str(e)}")
    
    def parse_course(self, response):
        inter_fee = response.xpath('(//div[contains(@class,"col-sm-6 col-md-2 course-fees__block international")]//p)[1]').get()
        cw = response.url
        duration = response.xpath('(//div[contains(@class,"course-details__summary")]//span[contains(@class,"international")]//text())[1]').get()
        study_load = response.xpath('(//div[contains(@class,"course-details__summary")]//span[contains(@class,"international")]//text())[2]').get()
        intake = response.xpath('//div[contains(@aria-label,"Dates")]//following-sibling::div').get()
        course_des = response.xpath('(//div[contains(@class,"text")]//p)[2]').get()
        carrer = response.xpath('(//div[contains(@class,"text-list")])[2]').get()
        course_struct = response.xpath('//table[contains(@class,"unit-table")]').getall()
        city = response.xpath('//div[contains(@class,"ourse-details__campus")]//div/text()').get()

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None


        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", cw)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)

        yield loader.load_item()


