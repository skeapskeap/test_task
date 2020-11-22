from selenium.webdriver.common.by import By


class YandexStartPageLocators():
    SEARCH_FIELD = '//input[@id="text"]'
    SUGGESTS = 'mini-suggest__popup-content'


class SearchResultsPageLocators():
    SEARCH_RESULTS = 'serp-item'
    LINKS_IN_RESULTS = 'link'
