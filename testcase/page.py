from element import SearchFieldElement
from locator import YandexStartPageLocators, SearchResultsPageLocators
from locator import PicturesPageLocators
from selenium.common import exceptions as exc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen
import hashlib


class BasePage():
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=5):
        wait = WebDriverWait(self.driver, time)
        try:
            element = wait.until(
                EC.presence_of_element_located(locator))
            return element
        except exc.TimeoutException:
            return False

    def find_elements(self, locator, time=5):
        wait = WebDriverWait(self.driver, time)
        try:
            elements = wait.until(
                EC.presence_of_all_elements_located(locator))
            return elements
        except exc.TimeoutException:
            return False

    def press_button(self, key):
        button = ActionChains(self.driver).send_keys(key)
        button.perform()


class YandexPage(BasePage):

    search_input = SearchFieldElement()

    def find_search_field(self):
        return self.find_element(
            YandexStartPageLocators.SEARCH_FIELD)

    def find_suggests(self):
        return self.find_element(
            YandexStartPageLocators.SUGGESTS)


class SearchResultPage(BasePage):

    def find_search_results(self):
        return self.find_elements(
            SearchResultsPageLocators.SEARCH_RESULTS)

    def keyword_in_results(self, keyword='tensor.ru', results_count=5):
        try:
            results = self.find_search_results()[:results_count]
        except IndexError:
            return False

        try:
            links = [
                    item.find_element_by_class_name(
                        SearchResultsPageLocators.LINKS_IN_RESULTS)
                    for item in results]
        except exc.NoSuchElementException:
            return False

        urls = [link.get_attribute('href') for link in links]
        match_keyword = list(filter(
            lambda url: keyword in url, urls
            ))
        if match_keyword:
            return True
        return False


class YandexPictures(BasePage):

    def find_pictures_icon(self):
        return self.find_element(
            PicturesPageLocators.PICTURES_ICON)

    def click_pics_icon(self):
        pics_icon = self.find_pictures_icon()
        if pics_icon:
            pics_icon.click()
            return True
        return False


class GaleryPage(BasePage):

    search_input = SearchFieldElement()

    def switch_window(self):
        win_list = self.driver.window_handles
        self.driver.switch_to.window(win_list[-1])

    def check_opened_url(self):
        current_url = self.driver.current_url
        return current_url.startswith(PicturesPageLocators.GALERY_URL)

    def open_first_category(self):
        first_category = self.find_element(
            PicturesPageLocators.GALERY_CATEGORIES)
        first_category_name = first_category.text
        first_category.click()
        opened_category_name = self.search_input
        return first_category_name == opened_category_name


class GaleryPictures(BasePage):

    images_hash = []

    def click_first_picture(self):
        first_picture = self.find_element(
            PicturesPageLocators.PICTRURES_IN_GALERY)
        if first_picture:
            first_picture.click()
            return True
        else:
            return False

    def check_opened_picture(self):
        opened_picture = self.find_element(
            PicturesPageLocators.OPENED_PICTURE)
        if opened_picture:
            GaleryPictures.get_hash(opened_picture)
            return True
        return False

    @staticmethod
    def get_hash(pic_obj):
        hasher = hashlib.md5()
        pic_url = pic_obj.get_attribute('src')
        img_file = urlopen(pic_url).read()
        hasher.update(img_file)
        img_hash = hasher.hexdigest()
        GaleryPictures.images_hash.append(img_hash)

    @staticmethod
    def compare_images():
        return GaleryPictures.images_hash[0] == GaleryPictures.images_hash[-1]
