import scrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from scrapy.http import Response

class BondSpider(scrapy.Spider):
    name = 'bon'
    file_name = 'Bond University 2025'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
    
    start_urls = ['https://bond.edu.au/study/program-finder?program_category%5B%5D=Undergraduate&program_category%5B%5D=Postgraduate&program_category%5B%5D=Postgraduate+research']

    def parse(self, response: Response):
        self.driver.get(response.url)

        courses = []
        try:
            for _ in range(16):  # Iterate through pages
                courses.extend([
                    course.get_attribute('href')
                    for course in self.driver.find_elements(By.XPATH, '//a[contains(@class,"uk-position-cover")]')
                ])
                btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '(//button[contains(@class,"uk-icon-button uk-icon btn-secondary icon-only")])[1]'))
                )
                btn.click()
        except TimeoutException:
            self.logger.info("Finished pagination.")
        except NoSuchElementException:
            self.logger.info("Pagination button not found.")

        self.logger.info(f"Collected {len(courses)} course URLs.")
        for course in courses:
            if course:
                yield scrapy.Request(course, callback=self.parse_course)

    def parse_course(self, response: Response):
        # Process individual course pages
        self.logger.info(f"Processing course page: {response.url}")

    
    def closed(self, reason):
        self.driver.quit()
