import scrapy

class UlsterSpider(scrapy.Spider):
    name = "uls"
    file_name = "University of Ulster 2025"
    
    start_urls = [
        "https://www.ulster.ac.uk/courses?query=&f.Level_u|Y=Postgraduate&f.Level_u|Y=Undergraduate&start_rank=1"
    ]

    def parse(self, response):
        courses = response.xpath('//a[contains(@class,"course-search-alpha__results")]/@href').getall()

        for course in courses:
            if course:
                yield response.follow(course, callback=self.parse1)

        self.logger.info(f"Total Courses: {len(courses)}")

        next_page = response.xpath('(//a[contains(@class,"course-search-alpha__pagination__link")])[2]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse1(self, response):
        print("Course_urls:", response.url)