import scrapy
from scrapy.loader import ItemLoader
from WebScraping.items import WebscrapingItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException


class CharlsSpider(scrapy.Spider):
    name = "charl"
    file_name = "Charles Sturt University 2025"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1920x1080")

        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )  # Custom User-Agent

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.driver.implicitly_wait(10)

    start_urls = ["https://study.csu.edu.au/international/courses"]

    def parse(self, response, **kwargs):
        self.driver.get(response.url)

        btn = self.driver.find_element(
            By.XPATH, '//button[contains(@id,"course-finder-show-more")]'
        )

        try:
            btn.click()
            for _ in range(16):
                btn.click()
        except:
            pass

        course_urls = self.driver.find_elements(
            By.XPATH, '//div[contains(@class,"course-result-title")]/a'
        )
        course_urls = [url.get_attribute("href") for url in course_urls]
        print(course_urls)

        for urls in course_urls:
            if urls:
                yield response.follow(
                    urls,
                    callback=self.parse1,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",  # Custom header for Scrapy requests
                    },
                )

    def parse1(self, response):
        self.driver.get(response.url)

        def safe_get_element(by, path):
            try:
                return self.driver.find_element(by, path).get_attribute("outerHTML")
            except (NoSuchElementException, WebDriverException) as e:
                print(f"Error fetching element {path}: {e}")
                return None

        course_des = safe_get_element(
            By.XPATH, '//div[contains(@class,"course-overview")]'
        )
        course_name = safe_get_element(
            By.XPATH, '//div[contains(@class,"course-name")]'
        )
        duration = safe_get_element(
            By.XPATH, '//span[contains(@class,"populate-duration")]'
        )
        inter_fee = safe_get_element(
            By.XPATH,
            '//div[contains(@class,"key-info-content populate-indicative-fees")]',
        )
        intake = safe_get_element(
            By.XPATH, '//div[contains(@class,"populate-all-session")]'
        )
        other = safe_get_element(
            By.XPATH, '//div[contains(@id,"academic_entry_requirements-content")]'
        )

        year = "2025" if inter_fee else None
        term = "Year" if inter_fee else None
        currency = "AUD" if inter_fee else None

        loader = ItemLoader(item=WebscrapingItem(), response=response)
        loader.add_value("Course_Name", course_name)
        loader.add_value("Course_Website", response.url)
        loader.add_value("International_Fee", inter_fee)
        loader.add_value("Course_Description", course_des)
        loader.add_value("Duration", duration)
        loader.add_value("Duration_Term", duration)
        loader.add_value("Intake_Month", intake)
        loader.add_value("Other_Requriment", other)
        loader.add_value("Fee_Year", year)
        loader.add_value("Fee_Term", term)
        loader.add_value("Currency", currency)

        yield loader.load_item()

    def close(self):
        self.driver.quit()
