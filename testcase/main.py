import unittest
from selenium import webdriver
import page
from time import sleep

PATH = "C:\\Py\\test_task\\chromedriver.exe"


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get('https://yandex.ru')
        self.verificationErrors = []

    def try_(self, func):
        try:
            self.assertTrue(func())
        except AssertionError:
            func_name = func.__name__
            self.verificationErrors.append(f'{func_name} FAILS =\\')

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        self.driver.quit()


class YandexSearch(BaseTest):

    def test_search(self):
        main_page = page.YandexStartPage(self.driver)
        self.try_(main_page.search_field_exists)
        main_page.search_input = 'Тензор'
        self.try_(main_page.suggests_exist)
        self.try_(main_page.press_enter)
        results_page = page.SearchResultPage(self.driver)
        self.try_(results_page.search_results_exist)
        self.try_(results_page.keyword_in_results)


class YandexPics(BaseTest):

    def test_pics(self):
        main_page = page.YandexPictures(self.driver)
        self.try_(main_page.pictures_icon_exists)
        self.try_(main_page.click_pics_icon)
        galery_page = page.GaleryPage(self.driver)
        galery_page.switch_window()
        self.try_(galery_page.check_opened_url)
        self.try_(galery_page.open_first_category)


if __name__ == '__main__':
    unittest.main()
