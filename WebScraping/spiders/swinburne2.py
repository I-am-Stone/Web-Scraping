from typing import Any, Dict, List, Optional, Iterator, Union
import scrapy
from scrapy.http import Response, Request
import json
from WebScraping.items import WebscrapingItem
from scrapy.loader import ItemLoader

def english_check(value) -> list[str]:
    # ietls, tofel, pte
    certificate = [['6.0','5.5','5.5','5.5','5.5'], ['64','8','7','16','18'],['50','42','42','42','42']]
    bachelor = [['6.0','6.0','6.0','6.0','6.0'],['64','13','12','18','21'],['50','50','50','50','50']]
    nursing = [['7.0','7.0','7.0','7.0','7.0'],['94','24','24','23','27'],['66','66','66','66','66']] #nursing and psychology o ielts, 1 tofel, 2 pte
    master = [['6.5','6.0','6.0','6.0','6.0'],['79','13','12','18','21'],['58','50','50','50','50']] # master exercise and sports, law
    teaching = [['7.5','7.0','7.0','7.0','7.0'],['94','24','27','24','27'],['66','66','76','76','66']] # master exercise and sports, law

    if "Bachelor of Nursing" and "Psychological Sciences" in value:
        return nursing
    elif "Master of Teaching" in value:
        return teaching
    elif "Bachelor" in value:
        return bachelor
    elif "Master" in value:
        return master
    elif "Certificate" and "Diploma" in value:
        return certificate

    else:
        print("nothing")



class SwinSpider(scrapy.Spider):
    name: str = 'swin1'
    file_name: str = 'Swinburne_University_2025_v2_2025 GG'
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
        course_name = response.xpath('//div[contains(@class,"course-details__title")]//h1').get()
        duration = response.xpath('(//div[contains(@class,"course-details__summary")]//span[contains(@class,"international")]//text())[1]').get()
        study_load = response.xpath('(//div[contains(@class,"course-details__summary")]//span[contains(@class,"international")]//text())[2]').get()
        intake = response.xpath('//div[contains(@aria-label,"Dates")]//following-sibling::div').get()
        course_des = response.xpath('(//div[contains(@class,"text")]//p)[2]').get()
        carrer = response.xpath('(//div[contains(@class,"text-list")])[2]').get()
        course_struct = response.xpath('//table[contains(@class,"unit-table")]').getall()
        city = response.xpath('//div[contains(@class,"course-details__campus")]//div[contains(@class,"international")]').get()

        sub_titile = response.xpath('//h2[contains(@class,"course-details__subtitle")]').get()

        if sub_titile:
            course_name = course_name + f"({sub_titile})"


        

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None



        english = english_check(course_name)

        print(city)



        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", cw)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Duration",duration)
        loader.add_value("Duration_Term",duration)
        loader.add_value("Study_Load",study_load)
        loader.add_value("Intake_Month", intake)
        loader.add_value("Course_Description", course_des)
        loader.add_value("Career",carrer)
        loader.add_value("Course_Structure", course_struct)
        loader.add_value("City", city)

        item = loader.load_item()
        print(f"Debug - Final city value: {item.get('City')}")
        # o index overall, 1 reading, 2 listing, 3 speaking, 4 writing
        loader.add_value('IELTS_Overall', english[0][0])
        loader.add_value('IELTS_Reading', english[0][1])
        loader.add_value('IELTS_Writing', english[0][4])
        loader.add_value('IELTS_Listening', english[0][2])
        loader.add_value('IELTS_Speaking', english[0][3])


        loader.add_value('TOEFL_Overall', english[1][0])
        loader.add_value('TOEFL_Reading', english[1][1])
        loader.add_value('TOEFL_Speaking', english[1][3])
        loader.add_value('TOEFL_Writing', english[1][4])
        loader.add_value('TOEFL_Listening', english[1][2])

        loader.add_value('PTE_Overall', english[2][0])
        loader.add_value('PTE_Reading', english[2][1])
        loader.add_value('PTE_Writing', english[2][4])
        loader.add_value('PTE_Listening', english[2][2])
        loader.add_value('PTE_Speaking', english[2][3])

        loader.add_value("Currency", currency)



        # yield loader.load_item()


