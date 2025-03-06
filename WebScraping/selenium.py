from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    TimeoutException,
)
import logging


class SeleniumBase:
    """
    Reusable selnium for using in diffrent spiders
    """


    def __init__(self):
        """
            Initializes the SeleniumBase class by setting up a headless Chrome WebDriver
            with specified options such as window size and user-agent. Installs the ChromeDriver
            using ChromeDriverManager and sets an implicit wait for the driver.

            Attributes:
                driver (webdriver.Chrome): The Chrome WebDriver instance configured with specified options.
        """

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.driver.implicitly_wait(10)
        self.logger = logging.getLogger(__name__)

    def get_page_urls(self, url, wait_time=10):
        """
        This Function navigates url and wait to load them
        It returns boolen values, If Ture page is loaded
        """
        try:
            self.driver.get(url)
        except WebDriverException as e:
            print(f"error Loading page {url}: {str(e)}")
            return False

    def using_wait(self, by, value, wait_time=10):
        """
        Finding Element in page and waiting for it to load
        """
        try:
            wait = WebDriverWait(self.driver, wait_time)
            btn = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[contains(@id,"tab_1_4")]')))
            if btn:
                self.logger.info(f"""
                    ------------------------
                    This is btn {btn}
                    ----------------------
                """)
                btn.click()
                element = wait.until(EC.presence_of_element_located((by, value)))
                return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error finding element {value}: {str(e)}")
            return None
    
    def list_using_wait(self, by, value, wait_time=10):
        """
        Finding Element in page and waiting for it to load
        """
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_all_elements_located((by, value)))
            return element
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error finding element {value}: {str(e)}")
            return None

    def getting_target_element(self, by, value, wait_time=10):
        """
        Getting target element from page and waiting for it to load
        
        
        :param by: a selenium.webdriver.common.by.By object
        :param value: a string representing the value to identify the element
        :param wait_time: an integer representing the time to wait for the element to load
        :return: the innerHTML of the element if found else None
        """
        element = self.using_wait(by, value, wait_time)
        if element:
            return element.get_attribute("innerHTML")
    
    
    def getting_target_elements(self, by, value, wait_time=10):
        elements = self.list_using_wait(by, value, wait_time)
        
        if elements:
            element_list = [element.get_attribute("innerHTML") for element in elements]
            return element_list
        else:
            return []
    
    def get_element_urls(self, by, value, wait_time=10):
        elements = self.list_using_wait(by, value, wait_time)
        if elements:
            urls_list = [element.get_attribute("href") for element in elements]
            return urls_list
        else:
            return []
    
    def scroll_list_using_wait(self, by, value, wait_time=10, max_scrolls=30, scroll_pause_time=2.0):
        try:
            wait = WebDriverWait(self.driver, wait_time)
            
            # Initial attempt to find elements
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            initial_count = len(elements)
            self.logger.info(f"Initially found {initial_count} elements")
            
            # Scroll multiple times with different techniques
            for scroll_num in range(max_scrolls):
                # Try different scroll methods alternately
                if scroll_num % 3 == 0:
                    # Method 1: Scroll to bottom
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                elif scroll_num % 3 == 1:
                    # Method 2: Scroll in increments
                    self.driver.execute_script(f"window.scrollBy(0, 1000);")
                else:
                    # Method 3: Scroll to specific point
                    scroll_point = (scroll_num + 1) * 1000
                    self.driver.execute_script(f"window.scrollTo(0, {scroll_point});")
                
                # Wait for content to load
                import time
                time.sleep(scroll_pause_time)
                
                # Check elements after scrolling
                elements = wait.until(EC.presence_of_all_elements_located((by, value)))
                current_count = len(elements)
                
                self.logger.info(f"Scroll #{scroll_num+1}: Found {current_count} elements")
                
                # If we've found all expected elements, we can stop
              
                    
                # If no new elements after several scrolls, try clicking a "load more" button if it exists
                if current_count == initial_count and scroll_num > 3:
                    try:
                        load_more = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Load more') or contains(text(), 'Show more')]")
                        if load_more and len(load_more) > 0:
                            self.logger.info("Attempting to click 'Load more' button")
                            load_more[0].click()
                            time.sleep(2)  # Wait after clicking
                    except Exception as e:
                        self.logger.info(f"No load more button found or error clicking it: {e}")
                
                initial_count = current_count
            
            self.logger.info(f"Scrolling complete. Found {len(elements)} elements after {max_scrolls} scrolls")
            return elements
            
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Error finding elements {value}: {str(e)}")
            return None
    



    def close_driver(self):
        self.driver.quit()
