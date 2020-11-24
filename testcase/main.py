from locator import CHROME_PATH
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import page
import unittest


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


class YandexSearch(BaseTest):

    def test_search(self):
        main_page = page.YandexPage(self.driver)
        self.try_(main_page.find_search_field)
        main_page.search_input = 'Тензор'
        self.try_(main_page.find_suggests)
        main_page.press_button(Keys.ENTER)
        results_page = page.SearchResultPage(self.driver)
        self.try_(results_page.find_search_results)
        self.try_(results_page.keyword_in_results)


class YandexPics(BaseTest):

    def test_pics(self):
        main_page = page.YandexPictures(self.driver)
        self.try_(main_page.find_pictures_icon)
        self.try_(main_page.click_pics_icon)

        galery_page = page.GaleryPage(self.driver)
        galery_page.switch_window()
        self.try_(galery_page.check_opened_url)
        self.try_(galery_page.open_first_category)

        pictures_page = page.GaleryPictures(self.driver)
        self.try_(pictures_page.click_first_picture)
        pictures_page.press_button(Keys.ESCAPE)
        # первые доли секунды вместо картинки отображается превью
        # с точно такими же атрибутами, но другим 'src'
        # более элегантного способа не родилось
        self.try_(pictures_page.click_first_picture)
        self.try_(pictures_page.check_opened_picture)
        pictures_page.press_button(Keys.RIGHT)
        self.try_(pictures_page.check_opened_picture)
        pictures_page.press_button(Keys.LEFT)
        self.try_(pictures_page.check_opened_picture)
        self.try_(page.GaleryPictures.compare_images)


if __name__ == '__main__':
    unittest.main()
