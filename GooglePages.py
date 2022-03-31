from BaseApp import BasePage
from selenium.webdriver.common.by import By


class GoogleSearchLocators:
    LOCATOR_GOOGLE_SEARCH_FIELD = (By.NAME, "q")
    LOCATOR_GOOGLE_SEARCH_BUTTON = (By.XPATH, "//div/center/input")
    LOCATOR_GOOGLE_URLS = (By.XPATH, '//cite')


class SearchHelper(BasePage):

    def enter_word(self, word):
        search_field = self.find_element(GoogleSearchLocators.LOCATOR_GOOGLE_SEARCH_FIELD)
        search_field.click()
        search_field.send_keys(word)
        return search_field

    def click_on_the_search_button(self):
        return self.find_element(GoogleSearchLocators.LOCATOR_GOOGLE_SEARCH_BUTTON).click()

    def get_urls(self):
        all_list = self.find_elements(GoogleSearchLocators.LOCATOR_GOOGLE_URLS, time=2)
        return [x.text for x in all_list if len(x.text) > 0]
