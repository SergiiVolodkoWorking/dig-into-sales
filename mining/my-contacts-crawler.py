import pandas as pd
from BrowserFactory import BrowserFactory
from BookmarkRepo import BookmarkRepo
from LinkedInProfileScrapper import LinkedInProfileScrapper, ShortScrappedProfile
import time
import os.path
import traceback

BATCH_SIZE = 10
bookmark_file = "./data/my_network_short_bookmark.txt"
target_data_file = "./data/my_network_short.csv"

def save_profile(profile):
    if not os.path.isfile(target_data_file):
        df = pd.DataFrame([], columns=profile.__dict__.keys())
        df.to_csv(target_data_file, index=True)
    df = pd.read_csv(target_data_file, index_col=0)
    df = df.append(profile.__dict__, ignore_index=True)
    df.to_csv(target_data_file, index=True)

if __name__ == "__main__":
    browser = BrowserFactory.create()
    scrapper = LinkedInProfileScrapper(browser)
    bookmarkRepo = BookmarkRepo(bookmark_file)

    try:
        bookmark = bookmarkRepo.load_bookmark()
        scrapper.go_to_my_connections()
        time.sleep(5)

        for i in range(bookmark, bookmark + BATCH_SIZE):
            scrapper.scroll_to_index(i)
            profile = scrapper.scrap_short_profile(i)
            print(profile.name, profile.link)
            save_profile(profile)
            bookmarkRepo.save_bookmark(i)

    except Exception as ex:
        print("------- ERROR ---------")
        print(ex)
        traceback.print_exc()
    finally:
        browser.quit()
        print('The flow is completed.')