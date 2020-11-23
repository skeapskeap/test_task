from locator import CHROME_PATH
from selenium import webdriver
import page
import unittest
from time import sleep


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(CHROME_PATH)
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

'''
class YandexSearch(BaseTest):

    def test_search(self):
        main_page = page.YandexPage(self.driver)
        self.try_(main_page.find_search_field)
        main_page.search_input = 'Тензор'
        self.try_(main_page.find_suggests)
        self.try_(main_page.press_enter)

        results_page = page.SearchResultPage(self.driver)
        self.try_(results_page.find_search_results)
        self.try_(results_page.keyword_in_results)
'''


class YandexPics(BaseTest):

    def test_pics(self):
        main_page = page.YandexPictures(self.driver)
        self.try_(main_page.find_pictures_icon)
        self.try_(main_page.click_pics_icon)

        galery_page = page.GaleryPage(self.driver)
        galery_page.switch_window()
        self.try_(galery_page.check_opened_url)
        self.try_(galery_page.open_first_category)

        pictures_page = page.PicturesPage(self.driver)
        self.try_(pictures_page.click_first_picture)
        self.try_(pictures_page.pic_open_success)
        sleep(2)
        pictures_page.press_arrow('right')
        self.try_(pictures_page.pic_open_success)
        sleep(2)
        pictures_page.press_arrow('left')
        self.try_(pictures_page.pic_open_success)
        sleep(2)
        self.try_(pictures_page.compare_images)
        sleep(2)


if __name__ == '__main__':
    unittest.main()
