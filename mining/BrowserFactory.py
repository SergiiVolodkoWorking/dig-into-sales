from selenium import webdriver

class BrowserFactory:
    @staticmethod
    def create():
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(90)

        return browser