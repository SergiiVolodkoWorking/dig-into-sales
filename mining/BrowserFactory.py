from selenium import webdriver
import os

class BrowserFactory:
    @staticmethod
    def create():
        # The profile is needed to stay logged in on the LinkedIn site
        directory = os.path.expanduser("~/Library/Application Support/Firefox/Profiles/")
        profile = [d for d in os.listdir(directory) if ".default-release" in d][0]
        my_profile = webdriver.FirefoxProfile(directory + profile)

        browser = webdriver.Firefox(my_profile)
        browser.set_page_load_timeout(90)

        return browser