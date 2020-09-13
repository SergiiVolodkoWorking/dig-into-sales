from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

class LinkedInEmailScrapper:
    browser = {}

    def __init__(self, browser):
        self.browser = browser

    def parse_property_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].text

    def go_to_my_connections(self):
        self.browser.get("https://www.linkedin.com//mynetwork/invite-connect/connections/")
        self.browser.find_elements(By.XPATH, "//button[@data-control-name='sort_by']")[0].click()
        self.browser.find_elements(By.XPATH, "//div[@aria-label='Sort connections by last name']")[0].click()
        time.sleep(3)

    def scroll_to_index(self, index_bookmark):
        profiles = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")
        html = self.browser.find_element_by_tag_name('html')
        SCROLL_PAUSE_TIME = 2
        while (len(profiles) < index_bookmark):
            html.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
            profiles = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")

    def open_profile(self, index):
        self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")[index].click()
        OPEN_PROFILE_PAUSE_TIME = 3
        time.sleep(OPEN_PROFILE_PAUSE_TIME)

    def scrap_contact_info(self):
        current_url = self.browser.current_url
        self.browser.get(current_url + "detail/contact-info/")
        time.sleep(1)
        print(self.parse_property_from_xpath("//a[contains(@href,'mailto:')]"))
        self.browser.get(current_url)
        time.sleep(1)
        