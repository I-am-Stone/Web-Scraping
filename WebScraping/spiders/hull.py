import re
import scrapy
import json 
from itemloaders import ItemLoader
from WebScraping.items import WebscrapingItem



class UOHSpider(scrapy.Spider):

    name = "uoh"

    file_name = "University of Hull"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }

    

    def start_requests(self):
        url = "https://cms-uni-hull.cloud.contensis.com/api/delivery/projects/website/entries/search?fields=entryTitle%2Ctitle%2Ckeywords%2Cdescription%2Csys%2CsearchContent%2Cthumbnail%2Csys.metadata.profileImage&orderBy=%5B%7B%22desc%22%3A%22sys.metadata.courseType%22%7D%5D&pageIndex=0&pageSize=300&where=%5B%7B%22field%22%3A%22sys.versionStatus%22%2C%22equalTo%22%3A%22published%22%7D%2C%7B%22field%22%3A%22sys.dataFormat%22%2C%22equalTo%22%3A%22webpage%22%7D%2C%7B%22field%22%3A%22sys.uri%22%2C%22startsWith%22%3A%22%2Fstudy%2F%22%7D%2C%7B%22field%22%3A%22sys.metadata.includeInSearch%22%2C%22equalTo%22%3Atrue%7D%2C%7B%22or%22%3A%5B%7B%22field%22%3A%22entryTitle%22%2C%22equalTo%22%3A%22%22%2C%22weight%22%3A10%7D%2C%7B%22field%22%3A%22entryTitle%22%2C%22startsWith%22%3A%22%22%2C%22weight%22%3A9%7D%2C%7B%22field%22%3A%22entryTitle%22%2C%22contains%22%3A%22%22%2C%22weight%22%3A8%7D%2C%7B%22field%22%3A%22entryTitle%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Atrue%2C%22operator%22%3A%22and%22%7D%2C%22weight%22%3A3%7D%2C%7B%22field%22%3A%22searchContent%22%2C%22contains%22%3A%22%22%2C%22weight%22%3A6%7D%2C%7B%22field%22%3A%22keywords%22%2C%22contains%22%3A%22%22%2C%22weight%22%3A3%7D%2C%7B%22or%22%3A%5B%7B%22field%22%3A%22description%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%2C%22weight%22%3A3%7D%2C%7B%22field%22%3A%22keywords%22%2C%22contains%22%3A%22%22%2C%22weight%22%3A3%7D%2C%7B%22field%22%3A%22searchContent%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.focusKeyphrase%22%2C%22equalTo%22%3A%22%22%2C%22weight%22%3A6%7D%2C%7B%22field%22%3A%22sys.metadata.focusKeyphrase%22%2C%22startsWith%22%3A%22%22%2C%22weight%22%3A6%7D%5D%7D%5D%7D%2C%7B%22and%22%3A%5B%7B%22field%22%3A%22sys.metadata.facultyArea%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.departmentArea%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.subjectArea%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.courseType%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.courseStart%22%2C%22contains%22%3A%220%2F1048%2F1052%2F1056%2F1252%22%7D%2C%7B%22field%22%3A%22sys.metadata.courseDuration%22%2C%22contains%22%3A%22%22%7D%2C%7B%22field%22%3A%22sys.metadata.courseVariation%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%7D%2C%7B%22field%22%3A%22sys.metadata.courseVariation%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%7D%2C%7B%22field%22%3A%22sys.metadata.courseVariation%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%7D%2C%7B%22field%22%3A%22sys.metadata.courseVariation%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%7D%2C%7B%22field%22%3A%22sys.metadata.clearing%22%2C%22freeText%22%3A%7B%22term%22%3A%22%22%2C%22fuzzy%22%3Afalse%2C%22operator%22%3A%22and%22%7D%7D%5D%7D%5D"
        headers = {
            "accesstoken": "rRdGBGOsFIIWzFDeXMz9Zf6gpSq8sidf5b2yeys4pqfDbQO7",
        }
        yield scrapy.Request(url, headers=headers)
    
    def parse(self, response):
        base_url = "https://www.hull.ac.uk"
        json_data = json.loads(response.text)
        for course in json_data["items"]: # 220 courses
            course_info = {}
            url = base_url+course["sys"]["uri"]
            try:
                course_info["Course_Name"] = course["entryTitle"]
            except:
                pass
            try:
                course_info["city"] = course["computedData"]["campuses"]
            except:
                pass
            yield response.follow(url, callback=self.parse1, meta={
                "course_info": course_info
            })

    def parse1(self, response):
        loader = ItemLoader(item=WebscrapingItem(), selector=response)
        
        course_info = response.meta.get("course_info")
        for key, value in course_info.items():
            loader.add_value(key, value)
        loader.add_value("Course_Website", response.url)

        intake_month = response.xpath("//div[contains(@class, 'info')]//p[contains(., 'Start in')]//text()").getall()
        if intake_month:
            loader.add_value("Intake_Month", intake_month)
        else:
            intake_month = response.xpath("//div[contains(.//p/@id, 'start-year') and contains(@class, 'dropdown-container')]//div[contains(@class, 'dp-content')]//li/text()").getall()
            if intake_month:
                loader.add_value("Intake_Month", intake_month)


        sl = response.xpath("//table[contains(@class, 'course-duration')]//th[contains(text(), 'time')]//text()").getall()
        study_load = ""
        if sl:
            for s in sl:
                study_load += s + ", "
            loader.add_value("Study_Load", study_load)

        duration = response.xpath("//table[contains(@class, 'course-duration')]//td[contains(text(), 'year') or contains(text(), 'month') or contains(text(), 'week') or contains(text(), 'day')]//text()").get()
        if duration:
            loader.add_value("Duration", duration)
            loader.add_value("Duration_Term", duration)
        
        loader.add_xpath("Course_Description", "//section[contains(@class, 'course-section')]//div[contains(@class, 'golden-large') and contains(.//h2//text(), 'About')]")
        yield loader.load_item()