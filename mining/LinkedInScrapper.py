from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re

class LinkedInScrapper:
    browser = {}

    def __init__(self, browser):
        self.browser = browser

    def parse_property_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].text

    def clean_description(self, text):
        text = text.replace('\n', ' ')
        text = text.replace('\t', '').replace('   ', '').replace('  ', ' ')
        # Uncamelcase
        result = re.sub("([a-z])([A-Z])","\g<1> \g<2>", text)
        return result

    def get_company_data(self, linked_company_url):
        self.browser.get(linked_company_url)
        established = self.parse_property_from_xpath("//dt[text()='Founded']/following::dd")

        specialties_text = self.parse_property_from_xpath("//dd[@dir='ltr']")
        specialties = specialties_text.replace(', and',',')
        
        size_text = self.parse_property_from_xpath("//dd[contains(@class,'org-about-company-module__company-size-definition-text')]")
        size = size_text[:size_text.find(' empl')].replace(' ','')
        
        description_text = self.parse_property_from_xpath("//section/p[@class='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal']")
        description = self.clean_description(description_text)

        industry = self.parse_property_from_xpath("//dt[text()='Industry']/following::dd")

        return description, size, specialties, established, industry