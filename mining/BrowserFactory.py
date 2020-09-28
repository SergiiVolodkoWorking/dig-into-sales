from selenium import webdriver
import os

class BrowserFactory:
    @staticmethod
    def create():
        # The profile is needed to stay logged in on the LinkedIn site
        directory = os.path.expanduser("~/Library/Application Support/Firefox/Profiles/")
        
        latest_profile = sorted(os.listdir(directory), key=lambda x: os.path.getctime(directory + x), reverse=True)[0]

        my_profile = webdriver.FirefoxProfile(directory + latest_profile)

        browser = webdriver.Firefox(my_profile)
        browser.set_page_load_timeout(90)

        return browser