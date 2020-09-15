import os.path
import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInProfileScrapper import LinkedInProfileScrapper
from LinkedInCompanyScrapper import LinkedInCompanyScrapper
import time

BATCH_SIZE = 1
bookmark_file = "./data/emails_bookmark.txt"

def save_bookmark(i):
    with open(bookmark_file, "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    if not os.path.isfile(bookmark_file):
        save_bookmark(0)
    with open(bookmark_file, "r") as file:
        return int(file.read())

# def go_back(browser):
#     time.sleep(3)
#     browser.execute_script("window.history.go(-1)")
#     time.sleep(3)

if __name__ == "__main__":
    browser = BrowserFactory.create()
    profileScrapper = LinkedInProfileScrapper(browser)
    companyScrapper = LinkedInCompanyScrapper(browser)

    try:
        bookmark = load_bookmark()
        profileScrapper.go_to_my_connections()
        
        for i in range(bookmark, bookmark + BATCH_SIZE):
            profileScrapper.scroll_to_index(i)
            profileScrapper.open_profile_by_index(i)
            profile = profileScrapper.scrap_contact_info()
            
            print(profile.name, profile.email)
            
            if('/company/' in profile.company_link or
               '/school/' in profile.company_link):
               company_url = profile.company_link + '/about'
               company = companyScrapper.get_company_data(company_url)
               print(company.specialties)
            
        # input("Press ENTER to finish.....")
    finally:
        browser.quit()
        print('The flow is completed.')
