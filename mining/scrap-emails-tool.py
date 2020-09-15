import os.path
import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInProfileScrapper import LinkedInProfileScrapper
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

def go_back(browser):
    time.sleep(3)
    browser.execute_script("window.history.go(-1)")
    time.sleep(3)

if __name__ == "__main__":
    browser = BrowserFactory.create()
    scrapper = LinkedInProfileScrapper(browser)

    try:
        bookmark = load_bookmark()
        scrapper.go_to_my_connections()
        
        for i in range(bookmark, bookmark + BATCH_SIZE):
            scrapper.scroll_to_index(i)
            scrapper.open_profile_by_index(i)
            profile = scrapper.scrap_contact_info()
            
            go_back(browser)
            print(profile.name, profile.email)
            
            # if(not '/comany/' in profile.company_link):
            #     continue
        input("Press ENTER to finish.....")
    finally:
        browser.quit()
        print('The flow is completed.')
