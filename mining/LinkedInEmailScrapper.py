from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re

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
