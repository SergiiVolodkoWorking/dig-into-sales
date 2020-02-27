from selenium import webdriver

class BrowserFactory:
    @staticmethod
    def create():
        my_profile = webdriver.FirefoxProfile('/Users/sergii.volodko/Library/Application Support/Firefox/Profiles/01i25ol7.default-release')
        browser = webdriver.Firefox(my_profile)
        browser.set_page_load_timeout(90)

        return browser