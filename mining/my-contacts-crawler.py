import pandas as pd
from BrowserFactory import BrowserFactory
from BookmarkRepo import BookmarkRepo
from LinkedInProfileScrapper import LinkedInProfileScrapper, ShortScrappedProfile
import time
import os.path
import traceback
from tqdm import tqdm

BATCH_SIZE = 1
firefox_profile = '/Users/sergii.volodko/Library/Application Support/Firefox/Profiles/01i25ol7.default-release'
bookmark_file = "./data/my_network_links_bookmark.txt"
target_data_file = "./data/my_network_links.csv"

def save_profile(profile):
    if not os.path.isfile(target_data_file):
        df = pd.DataFrame([], columns=profile.__dict__.keys())
        df.to_csv(target_data_file, index=True)
    df = pd.read_csv(target_data_file, index_col=0)
    df = df.append(profile.__dict__, ignore_index=True)
    df.to_csv(target_data_file, index=True)

if __name__ == "__main__":
    print("\n\n----------- Script started -----------\n")
    print(" Welcome to the contacts crawler!\n")
    print(" The script will scroll through your LinkedIn contacts in Firefox\n")
    print(" And save the links to {}\n".format(target_data_file))
    print(" Please make sure you are logged in to LinkedIn in your Firefox\n")
    print("\n--------------------------------------\n")
    print("Launching...\n")
    browser = BrowserFactory.create(firefox_profile)
    scrapper = LinkedInProfileScrapper(browser)
    bookmarkRepo = BookmarkRepo(bookmark_file)

    try:
        print("Scrapping your next {} contacts".format(BATCH_SIZE))
        bookmark = bookmarkRepo.load_bookmark()
        scrapper.go_to_my_connections()
        totalConnections = scrapper.scrap_contacts_number()
        print("Bookmarked progress {} / {}".format(bookmark, totalConnections))
        time.sleep(5)

        print("Scrolling to {} ...".format(bookmark))
        print("Note: sometimes automatic scroll can stuck. Please help the script with a manual scroll in that case")

        total = int(totalConnections.replace(' Connections', ''))

        for i in tqdm(range(bookmark, min(bookmark + BATCH_SIZE, total))):
            scrapper.scroll_to_index(i)
            profile = scrapper.scrap_short_profile(i)
            save_profile(profile)
            bookmarkRepo.save_bookmark(i)

    except Exception as ex:
        print("----------- ERROR -----------")
        print(ex)
        traceback.print_exc()
    finally:
        browser.quit()
        print("\n----------- Script finished -----------\n")