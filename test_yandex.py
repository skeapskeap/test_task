from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as ex
from time import sleep
from urllib.request import urlretrieve
import hashlib
import unittest


PATH = "C:\\Py\\test_task\\chromedriver.exe"
IMG_DIR = "C:\\Py\\test_task\\images\\"


def get_hash(file):
    hasher = hashlib.md5()
    # read file as binary
    with open(file, 'rb') as f:
        hasher.update(f.read())
        return hasher.hexdigest()


class Yandex(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get('https://yandex.ru')

    def test_01(self):
        driver = self.driver

        # проверка наличия поля поиска
        try:
            search_field = driver.find_element_by_xpath('//input[@id="text"]')
        except ex.NoSuchElementException:
            raise AssertionError('Нет поля поиска')

        # проверка наличия подсказок
        search_field.send_keys('Тензор')
        sleep(1)
        try:
            driver.find_element_by_class_name("mini-suggest__popup-content")
        except ex.NoSuchElementException:
            raise AssertionError('Нет подсказок поиска')

        search_field.send_keys(Keys.ENTER)
        sleep(3)

        # проверка наличия результатов поиска
        try:
            results = driver.find_elements_by_class_name('serp-item')[:5]
            first_five = results[:5]
        except ex.NoSuchElementException:
            raise AssertionError('Нет результатов поиска')

        # проверка наличия ссылок в результатах поиска
        try:
            links = [
                item.find_element_by_class_name('link') for item in first_five
                ]
            self.urls = [link.get_attribute('href') for link in links]
        except ex.NoSuchElementException:
            raise AssertionError('В результатах поиска нет ссылок')

        # проверка вхождения tensor.ru в результаты поиска
        match = list(filter(lambda url: 'tensor.ru' in url, self.urls))
        if not match:
            raise AssertionError('tensor.ru нет в результатах поиска')

        assert True

    def test_02(self):
        driver = self.driver

        # Проверка наличия ссылки на картинки
        try:
            images = driver.find_element_by_xpath('//a[@data-id="images"]')
        except ex.NoSuchElementException:
            raise AssertionError('Нет ссылки на картинки')

        images.click()
        sleep(2)

        # картинки должны открыться в новом окне
        try:
            # выбираем вторую из открытых вкладок
            new_win = driver.window_handles[1]
            # говорим драйверу смотреть на неё
            driver.switch_to.window(new_win)
        except IndexError:
            raise AssertionError('Картинки не открылись')

        # проверка открытого URL
        if not driver.current_url.startswith('https://yandex.ru/images/'):
            raise AssertionError('Открылись не картинки')

        # запоминаем имя первой категории если это возможно
        try:
            firts_category = driver.find_element_by_xpath(
                '//div[@class="PopularRequestList-SearchText"]'
                )
            firts_category_name = firts_category.text
            firts_category.click()
            sleep(2)
        except ex.NoSuchElementException:
            raise AssertionError('Нет категорий')

        # совпадение слов в поисковой строке с выбранной категорией
        try:
            search_field = driver.find_element_by_xpath(
                '//input[@class="input__control"]'
                )
            opened_category = search_field.get_attribute('value')
            if not opened_category == firts_category_name:
                raise AssertionError('Открылась не та категория')
        except ex.NoSuchElementException:
            raise AssertionError('В открытой категории нет поля поиска')

        # ищем и переходим на первую картину в открытой категории
        try:
            first_pic = driver.find_element_by_xpath(
                '//a[@class="serp-item__link"]'
                )
            first_pic.click()
            sleep(3)
        except ex.NoSuchElementException:
            raise AssertionError('Не получилось найти первую картинку')

        # проверка того, что картинка открылась
        try:
            current_pic = driver.find_element_by_xpath(
                '//img[@class="MMImage-Origin"]'
                )
            pic_url = current_pic.get_attribute('src')
        except ex.NoSuchElementException:
            raise AssertionError('Первая картинка в категории не открылась')

        # грузим первую картинку и считаем её хэш
        first_img_file = f'{IMG_DIR}first.pic'
        urlretrieve(pic_url, first_img_file)
        first_hash = get_hash(first_img_file)

        # стрелочка вправо ->
        right = ActionChains(driver).send_keys(Keys.RIGHT)
        right.perform()
        sleep(1)

        # проверка того, что по нажатию Right картинка открылась
        try:
            next_pic = driver.find_element_by_xpath(
                '//img[@class="MMImage-Origin"]'
                )
            next_url = next_pic.get_attribute('src')
        except ex.NoSuchElementException:
            raise AssertionError('Следующая картинка в категории не открылась')

        # грузим второй рисунок и считаем его хэш
        next_img_file = f'{IMG_DIR}next.pic'
        urlretrieve(next_url, next_img_file)
        next_hash = get_hash(next_img_file)

        # проверка того, что картинка имзенилась
        if next_hash == first_hash:
            raise AssertionError('По нажатию Right картинка не изменилась')

        # стрелочка влево <-
        left = ActionChains(driver).send_keys(Keys.LEFT)
        left.perform()
        sleep(1)

        # проверка того, что по нажатию Left картинка открылась
        try:
            prev_pic = driver.find_element_by_xpath(
                '//img[@class="MMImage-Origin"]'
                )
            prev_url = prev_pic.get_attribute('src')
        except ex.NoSuchElementException:
            raise AssertionError('Исходная картинка в категории не открылась')

        # снова грузим первый рисунок
        prev_img_file = f'{IMG_DIR}prev.pic'
        urlretrieve(prev_url, prev_img_file)
        prev_hash = get_hash(prev_img_file)

        # сравним хэши
        if first_hash == prev_hash:
            assert True
        else:
            raise AssertionError('Изображение после Right+Left изменилось')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
