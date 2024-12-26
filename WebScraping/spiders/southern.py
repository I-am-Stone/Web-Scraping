import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from urllib.parse import urlparse, parse_qs

class CrossSpider(scrapy.Spider):
    name = 'ros'
    file_name = 'Southern Cross University 2025'
    start_urls = ['https://www.scu.edu.au/study/international-courses-and-fees/']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = webdriver.ChromeOptions()
        # Add options to make browser more stable/efficient
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(10)

    def extract_real_url(self, redirect_url):
        """Extract the actual SCU course URL from the redirect URL"""
        try:
            parsed = urlparse(redirect_url)
            query_params = parse_qs(parsed.query)
            if 'url' in query_params:
                return query_params['url'][0]
        except Exception as e:
            self.logger.error(f"Error extracting URL: {e}")
            return None
        return None

    def parse(self, response):
        try:
            self.driver.get(response.url)
            # Wait for course cards to be visible
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"course-card course-card--wide")]//a'))
            )
            
            courses = self.driver.find_elements(By.XPATH, '//div[contains(@class,"course-card course-card--wide")]//a')
            course_urls = []
            
            for course in courses:
                redirect_url = course.get_attribute('href')
                if redirect_url:
                    actual_url = self.extract_real_url(redirect_url)
                    if actual_url:
                        course_urls.append(actual_url)
            
            self.logger.info(f"Found {len(course_urls)} course URLs")
            
            # Use Selenium for each course page since we're already using it
            for url in course_urls:
                try:
                    self.driver.get(url)
                    yield self.parse_course_page(url)
                except Exception as e:
                    self.logger.error(f"Error processing course page {url}: {e}")
            
            # Handle pagination if it exists
            try:
                next_button = self.driver.find_element(By.XPATH, '//ul[contains(@class,"pagination")]/li/a[contains(text(), "Next")]')
                if next_button and next_button.is_displayed():
                    next_url = next_button.get_attribute('href')
                    if next_url:
                        yield response.follow(next_url, callback=self.parse)
            except NoSuchElementException:
                self.logger.info("No next page found")
                
        except Exception as e:
            self.logger.error(f"Error in parse method: {e}")
        
    def parse_course_page(self, url):
        """Parse individual course page and extract required information"""
        try:
            # Wait for essential elements to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
            )
            
            # Extract course information
            course_data = {
                'url': url,
                'title': self.safe_extract('//h1/text()'),
                # Add more fields as needed
            }
            
            return course_data
            
        except Exception as e:
            self.logger.error(f"Error parsing course page: {e}")
            return None
            
    def safe_extract(self, xpath, default=''):
        """Safely extract text using Selenium"""
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element.text.strip()
        except:
            return default

    def closed(self, reason):
        """Clean up Selenium driver when spider closes"""
        if hasattr(self, 'driver'):
            self.driver.quit()