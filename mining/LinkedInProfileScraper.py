from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import sys
from random import uniform

class LinkedInProfileScraper:
    browser = {}

    def __init__(self, browser):
        self.browser = browser

    def parse_property_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].text

    def parse_href_from_xpath(self, path):
        elements = self.browser.find_elements(By.XPATH, path)
        return "" if len(elements) == 0 else elements[0].get_attribute("href")

    def go_to_my_connections(self):
        self.browser.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        # self.browser.find_elements(By.XPATH, "//button[@data-control-name='sort_by']")[0].click()
        # self.browser.find_elements(By.XPATH, "//div[@aria-label='Sort connections by last name']")[0].click()
        # time.sleep(3)

    def scrape_contacts_number(self):
       return self.parse_property_from_xpath("//h1[@class='t-18 t-black t-normal']")

    def scroll_to_index(self, index_bookmark):
        profiles = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")
        html = self.browser.find_element_by_tag_name('html')
        SCROLL_PAUSE_TIME = uniform(4.01, 6.3311)
        while (len(profiles) <= index_bookmark):
            html.send_keys(Keys.HOME)
            time.sleep(SCROLL_PAUSE_TIME - 3.75)
            html.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
            profiles = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")

    def open_profile_by_index(self, index):
        self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']")[index].click()
        OPEN_PROFILE_PAUSE_TIME = 3
        time.sleep(OPEN_PROFILE_PAUSE_TIME)

    def scrap_contact_info(self, profile_url):
        self.browser.get(profile_url)
        time.sleep(3)
        html = self.browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(3)

        name = self.parse_property_from_xpath("//li[@class='inline t-24 t-black t-normal break-words']")
        position = self.parse_property_from_xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']")
        location = self.parse_property_from_xpath("//li[@class='t-16 t-black t-normal inline-block']")
        company_link = self.parse_href_from_xpath("//a[@data-control-name='background_details_company']")
        company_link_info = self.parse_property_from_xpath("//a[@data-control-name='background_details_company']")

        self.browser.get(profile_url + "detail/contact-info/")
        time.sleep(1)

        linkedin_id = self.parse_property_from_xpath("//a[contains(@href,'https://www.linkedin.com/in')]")
        email = self.parse_property_from_xpath("//a[contains(@href,'mailto:')]")
        phone = self.parse_property_from_xpath("//li/span[@class='t-14 t-black t-normal']")
        website = self.parse_property_from_xpath("//section[@class='pv-contact-info__contact-type ci-websites']/ul")

        return ScrappedProfile(linkedin_id, name, position, email, phone, website, location, company_link)

    def scrape_short_profile(self, index):
        link = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']/a")[index].get_attribute("href")
        description = self.browser.find_elements(By.XPATH, "//li[@class='mn-connection-card artdeco-list ember-view']/div/a")[index].text
        name, occupation = description.split("\nMember’s occupation\n")
        name = name.replace("Member’s name\n", "")

        return ShortScrapedProfile(link, name, occupation)


class ShortScrapedProfile:
    def __init__(self, link, name, occupation):
        self.name = name
        self.occupation = occupation
        self.link = link

class ScrappedProfile:
    def __init__(self, linkedin_id, name, occupation, email, phone, website, location, company_link):
        self.linkedin_id = linkedin_id
        self.name = name
        self.occupation = occupation
        self.email = email
        self.phone = phone
        self.website = website
        self.location = location
        self.company_link = company_link