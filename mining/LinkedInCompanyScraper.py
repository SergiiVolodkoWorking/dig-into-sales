from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time

class LinkedInCompanyScraper:
    browser = {}

    def __init__(self, browser):
        self.browser = browser

    def parse_property_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].text

    def parse_image_src_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].get_attribute("src")

    def clean_description(self, text):
        text = text.replace('\n', ' ')
        text = text.replace('\t', '').replace('   ', '').replace('  ', ' ')
        # Uncamelcase
        result = re.sub("([a-z])([A-Z])","\g<1> \g<2>", text)
        return result

    def get_company_data(self, linked_company_url):
        self.browser.get(linked_company_url)
        time.sleep(3)
        url = self.browser.current_url
        linkedin_id = 'unavailable' if url.endswith('unavailable/') else url.split('/')[-3]

        established = self.parse_property_from_xpath("//dt[text()='Founded']/following::dd")

        specialties_text = self.parse_property_from_xpath("//dd[@dir='ltr']")
        specialties = specialties_text.replace(', and',',')
        
        size_text = self.parse_property_from_xpath("//dd[contains(@class,'org-about-company-module__company-size-definition-text')]")
        size = size_text[:size_text.find(' empl')].replace(' ','')
        
        description_text = self.parse_property_from_xpath("//section/p[@class='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal']")
        description = self.clean_description(description_text)

        industry = self.parse_property_from_xpath("//dt[text()='Industry']/following::dd")
        website = self.parse_property_from_xpath("//dt[text()='Website']/following::dd")
        
        headquarter = self.parse_property_from_xpath("//div[@class='org-top-card-summary-info-list t-14 t-black--light']/div[contains(@class,'inline-block')]/div")
        if "followers" in headquarter:
            headquarter = ""

        logo_url = self.parse_image_src_from_xpath("//img[@class='org-top-card-primary-content__logo Elevation-0dp lazy-image ember-view']")
        company_name = self.parse_property_from_xpath("//h1/span[@dir='ltr']")

        return ScrapedCompany(linkedin_id,company_name, description, size, specialties, established, industry, website, headquarter, logo_url)

class ScrapedCompany:
    def __init__(self, linkedin_id, company_name, description, size, specialties, established, industry, website, headquarter, logo_url):
        self.linkedin_id = linkedin_id
        self.linkedin_name = company_name
        self.description = description
        self.size = size
        self.specialties = specialties
        self.established = established
        self.industry = industry
        self.website = website
        self.headquarter = headquarter
        self.logo_url = logo_url

class EmptyScrapedCompany(ScrapedCompany):
    def __init__(self):
        super(EmptyScrapedCompany, self).__init__("","","","","","","","","","")