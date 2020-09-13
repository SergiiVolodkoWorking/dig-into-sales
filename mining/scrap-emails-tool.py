import os.path
import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInEmailScrapper import LinkedInEmailScrapper


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
    scrapper = LinkedInEmailScrapper(browser)

    try:
        scrapper.go_to_my_connections()
        input("Press Enter to continue...")
    finally:
        browser.quit()
        print('The flow is completed.')
    


