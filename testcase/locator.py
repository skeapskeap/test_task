from selenium.webdriver.common.by import By


class YandexStartPageLocators():
    SEARCH_FIELD = '//input[@id="text"]'
    SUGGESTS = 'mini-suggest__popup-content'


class SearchResultsPageLocators():
    SEARCH_RESULTS = 'serp-item'
    LINKS_IN_RESULTS = 'link'


class PicturesPageLocators():
    PICTURES_ICON = '//a[@data-id="images"]'
    GALERY_CATEGORIES = '//div[@class="PopularRequestList-SearchText"]'
    GALERY_SEARCH_FIELD = '//input[@class="input__control"]'
