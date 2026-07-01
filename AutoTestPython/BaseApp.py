import logging
import yaml
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("./testdata.yaml") as f:
    data = yaml.safe_load(f)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = data["base_url"]

    def find_element(self, locator, time=10):
        try:
            element = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(locator),
                message=f"Element '{locator}' not found"
            )
        except Exception as e:
            logging.exception(f"Element '{locator}' not found: {str(e)}")
            element = None
        return element

    def get_element_property(self, locator, prop):
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(prop)
        else:
            logging.error(f"Property {prop} not found in element with locator {locator}")
            return None

    def go_to_site(self):
        try:
            self.driver.get(self.base_url)
            return True
        except Exception as e:
            logging.exception(f"Failed to start browser: {str(e)}")
            return False