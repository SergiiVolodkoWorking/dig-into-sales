import os.path
import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInProfileScrapper import LinkedInProfileScrapper
import time

BATCH_SIZE = 2
bookmark_file = "./data/emails_bookmark.txt"

def save_bookmark(i):
    with open(bookmark_file, "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    if not os.path.isfile(bookmark_file):
        save_bookmark(0)
    with open(bookmark_file, "r") as file:
        return int(file.read())

if __name__ == "__main__":
    browser = BrowserFactory.create()
    scrapper = LinkedInProfileScrapper(browser)
    
    try:
        bookmark = load_bookmark()
        scrapper.go_to_my_connections()

        for i in range(bookmark, bookmark + BATCH_SIZE):
            scrapper.scroll_to_index(i)
            profile = scrapper.scrap_short_profile(i)
            print(profile.name, profile.link)

    except Exception as ex:
        print("------- ERROR ---------")
        print(ex)
    finally:
        browser.quit()
        print('The flow is completed.')