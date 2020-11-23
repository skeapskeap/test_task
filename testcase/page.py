from element import SearchFieldElement
from locator import YandexStartPageLocators, SearchResultsPageLocators
from locator import PicturesPageLocators, IMG_FILE
from selenium.common import exceptions as exc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlretrieve
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


class YandexPage(BasePage):

    search_input = SearchFieldElement()

    def find_search_field(self):
        return self.find_element(
            YandexStartPageLocators.SEARCH_FIELD)

    def find_suggests(self):
        return self.find_element(
            YandexStartPageLocators.SUGGESTS)

    def press_enter(self):
        search_field = self.find_search_field()
        if search_field:
            search_field.send_keys(Keys.ENTER)
            return True
        return False


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
        if current_url.startswith('https://yandex.ru/images/'):
            return True
        return False

    def open_first_category(self):
        first_category = self.find_element(
            PicturesPageLocators.GALERY_CATEGORIES)
        first_category_name = first_category.text
        first_category.click()
        opened_category_name = self.search_input
        if first_category_name == opened_category_name:
            return True
        return False


class PicturesPage(BasePage):

    images_hash = []

    def click_first_picture(self):
        first_picture = self.find_element(
            PicturesPageLocators.PICTRURES_IN_GALERY)
        if first_picture:
            first_picture.click()
            return True
        else:
            return False

    def pic_open_success(self):
        opened_picture = self.find_element(
            PicturesPageLocators.OPENED_PICTURE)
        if opened_picture:
            self.get_hash(opened_picture)
            return True
        return False

    def get_hash(self, pic_obj):
        pic_url = pic_obj.get_attribute('src')
        urlretrieve(pic_url, IMG_FILE)
        hasher = hashlib.md5()
        # read file as binary
        with open(IMG_FILE, 'rb') as f:
            hasher.update(f.read())
            self.images_hash.append(hasher.hexdigest())
            print(self.images_hash)

    def press_arrow(self, direction='right'):
        if direction == 'left':
            arrow = ActionChains(self.driver).send_keys(Keys.LEFT)
        else:
            arrow = ActionChains(self.driver).send_keys(Keys.RIGHT)
        arrow.perform()

    def compare_images(self):
        if self.images_hash[0] == self.images_hash[-1]:
            return True
        return False
