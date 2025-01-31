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
        element = self.using_wait(by, value, wait_time)
        return element.get_attribute("outerHTML") if element else None
    
    def get_element_urls(self, by, value, wait_time=10):
        elements = self.list_using_wait(by, value, wait_time)
        if elements:
            urls_list = [element.get_attribute("href") for element in elements]
            return urls_list
        else:
            return []

    def close_driver(self):
        self.driver.quit()
