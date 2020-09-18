from selenium import webdriver

class BrowserFactory:
    @staticmethod
    def create(fireFoxProfile='/Users/sergii.volodko/Library/Application Support/Firefox/Profiles/01i25ol7.default-release'):
        # The profile is needed to stay logged in to LinkedIn site
        my_profile = webdriver.FirefoxProfile(fireFoxProfile)
        browser = webdriver.Firefox(my_profile)
        browser.set_page_load_timeout(90)

        return browser