from selenium.webdriver.support.ui import WebDriverWait
import locator


class BasePageElement():
    def __set__(self, obj, value):
        driver = obj.driver
        wait = WebDriverWait(driver, 5)
        wait.until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        wait = WebDriverWait(driver, 5)
        wait.until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute('value')


class SearchFieldElement(BasePageElement):
    locator = 'text'


class GaleryPageElement(BasePageElement):
    def __init__(self, driver):
        wait = WebDriverWait(driver, 5)
        self.first_category = wait.until(
            lambda driver: driver.find_element_by_xpath(
                locator.PicturesPageLocators.GALERY_CATEGORIES))
        try:
            self.first_category_name = self.first_category.text
        except AttributeError:
            self.first_category_name = False
        self.opened_category_name = None

    def opened_category_correct(self):
        if self.first_category_name == self.opened_category_name:
            return True
        return False
