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
    GALLERY_URL = 'https://yandex.ru/images/'
    GALLERY_CATEGORIES = (By.XPATH, '//div[@class="PopularRequestList-SearchText"]')
    PICTRURES_IN_GALLERY = (By.XPATH, '//a[@class="serp-item__link"]')
    OPENED_PICTURE = (By.XPATH, '//img[@class="MMImage-Origin"]')
