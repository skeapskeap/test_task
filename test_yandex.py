from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex
from time import sleep
import unittest

PATH = "C:\\Py\\test_task\\chromedriver.exe"


class Yandex(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get('https://yandex.ru')

    def test_01(self):
        driver = self.driver

        try:
            search_field = driver.find_element_by_xpath('//*[@id="text"]')
        except ex.NoSuchElementException:
            raise AssertionError('Нет поля поиска')

        search_field.send_keys('Тензор')
        sleep(1)
        try:
            driver.find_element_by_class_name("mini-suggest__popup-content")
        except ex.NoSuchElementException:
            raise AssertionError('Нет подсказок поиска')

        search_field.send_keys(Keys.ENTER)
        sleep(3)

        try:
            search_results = driver.find_elements_by_class_name('serp-item')[:5]
        except ex.NoSuchElementException:
            raise AssertionError('Нет результатов поиска')

        try:
            links = [item.find_element_by_class_name('link') for item in search_results]
            self.urls = [link.get_attribute('href') for link in links]
        except ex.NoSuchElementException:
            raise AssertionError('В результатах поиска нет ссылок')

        for url in self.urls:
            print(url)
            if 'tensorк.ru' in url:
                break
        else:
            raise AssertionError('tensor.ru нет в результатах поиска')

        assert True

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
