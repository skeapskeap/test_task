from selenium.webdriver.common.by import By

CHROME_PATH = "abs path to chromedriver.exe"


class YandexStartPageLocators():
    SEARCH_FIELD = (By.XPATH, '//input[@id="text"]')
    SUGGESTS = (By.CLASS_NAME, 'mini-suggest__popup-content')


class SearchResultsPageLocators():
    SEARCH_RESULTS = (By.CLASS_NAME, 'serp-item')
    LINKS_IN_RESULTS = 'link'


class PicturesPageLocators():
    PICTURES_ICON = (By.XPATH, '//a[@data-id="images"]')
    GALERY_URL = 'https://yandex.ru/images/'
    GALERY_CATEGORIES = (By.XPATH, '//div[@class="PopularRequestList-SearchText"]')
    PICTRURES_IN_GALERY = (By.XPATH, '//a[@class="serp-item__link"]')
    OPENED_PICTURE = (By.XPATH, '//img[@class="MMImage-Origin"]')
