import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
import time
from random import uniform
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status == 403:
            spider.logger.info(f"Retrying {request.url} due to {response.status}")
            return self._retry(request, '403', spider) or response
        return response

class SouthWalesSpider(scrapy.Spider):
    name = "south_wales"
    file_name = "University_of_South_Wales"
    start_urls = ["https://www.southwales.ac.uk/courses"]
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # Temporarily disable while debugging
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 20,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [403, 429, 500, 502, 503, 504],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'WebScraping.spiders.south_wales.CustomRetryMiddleware': 550,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
    }
    
    def get_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'Cache-Control': 'max-age=0',
        }

    def start_requests(self):
        # First, try to establish a session
        return [
            scrapy.Request(
                'https://www.southwales.ac.uk',  # Start with homepage
                callback=self.after_homepage,
                headers=self.get_headers(),
                meta={
                    'dont_redirect': False,
                    'handle_httpstatus_list': [403, 404, 429, 500, 502, 503, 504]
                },
                dont_filter=True,
                errback=self.handle_error
            )
        ]

    def after_homepage(self, response):
        if response.status == 403:
            self.logger.error("Still getting 403 after homepage visit. Might need manual intervention.")
            return
            
        # Add a realistic delay
        time.sleep(uniform(4, 7))
        
        # Now try the courses page
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            headers=self.get_headers(),
            meta={
                'dont_redirect': False,
                'handle_httpstatus_list': [403, 404, 429, 500, 502, 503, 504]
            },
            dont_filter=True,
            errback=self.handle_error
        )

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"Access denied to {response.url}")
            return
            
        self.logger.info(f"Successfully accessed {response.url}")
        
        # Add random delay between requests
        time.sleep(uniform(4, 7))
        
        courses = response.xpath('//a[contains(@class,"h3")]/@href').getall()
        
        if not courses:
            self.logger.warning(f"No courses found on {response.url}. Checking alternative selectors...")
            # Try alternative selectors if the main one fails
            courses = response.xpath('//div[contains(@class,"course")]//a/@href').getall()
        
        for course in courses:
            if course:
                course_url = response.urljoin(course)
                yield scrapy.Request(
                    url=course_url,
                    callback=self.parse_course,
                    headers=self.get_headers(),
                    meta={'dont_redirect': False},
                    errback=self.handle_error
                )

        next_page_links = response.xpath('//nav[contains(@class,"pagination")]//a/@href').getall()
        for page in next_page_links:
            if page:
                next_url = response.urljoin(page)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    headers=self.get_headers(),
                    meta={'dont_redirect': False},
                    errback=self.handle_error
                )

    def parse_course(self, response):
        if response.status == 403:
            self.logger.error(f"Access denied to course page: {response.url}")
            return
            
        self.logger.info(f"Parsing course: {response.url}")
        
        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Website", response.url)
        
        yield loader.load_item()

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(f"Error: {failure.value}")