from locator import YandexStartPageLocators, SearchResultsPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions as exc
from selenium.webdriver.common.keys import Keys
from element import BasePageElement


class SearchFieldElement(BasePageElement):
    locator = 'text'


class BasePage():
    def __init__(self, driver):
        self.driver = driver


class YandexStartPage(BasePage):

    search_input = SearchFieldElement()

    def search_field_exists(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(
                lambda driver: self.driver.find_element_by_xpath(
                    YandexStartPageLocators.SEARCH_FIELD))
            return True
        except exc.TimeoutException:
            return False

    def suggests_exist(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(
                lambda driver: self.driver.find_element_by_class_name(
                    YandexStartPageLocators.SUGGESTS))
            return True
        except exc.TimeoutException:
            return False

    def press_enter(self):
        try:
            search = self.driver.find_element_by_xpath(
                YandexStartPageLocators.SEARCH_FIELD)
            search.send_keys(Keys.ENTER)
            return True
        except exc.NoSuchElementException:
            return False


class SearchResultPage(BasePage):

    def search_results_exist(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(
                lambda driver: self.driver.find_elements_by_class_name(
                    SearchResultsPageLocators.SEARCH_RESULTS))
            return True
        except exc.TimeoutException:
            return False

    def get_n_results(self, n):
        results = self.driver.find_elements_by_class_name(
                    SearchResultsPageLocators.SEARCH_RESULTS)
        return results[:n]

    def keyword_in_results(self, keyword='tensor.ru', n_results=5):
        results = self.get_n_results(n_results)
        try:
            links = [
                 item.find_element_by_class_name(
                    SearchResultsPageLocators.LINKS_IN_RESULTS
                    ) for item in results]
        except exc.NoSuchElementException:
            return False

        urls = [link.get_attribute('href') for link in links]

        match = list(filter(lambda url: keyword in url, urls))

        if not match:
            return False
        return True
