import pandas as pd
from BrowserFactory import BrowserFactory
from BookmarkRepo import BookmarkRepo
from LinkedInProfileScraper import LinkedInProfileScraper, ShortScrapedProfile
import time
import os.path
import traceback
from tqdm import tqdm
import json

root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FOLDER = os.path.join(root_folder, "data")

def save_profile(profile, target_file):
    if not os.path.isfile(target_file):
        df = pd.DataFrame([], columns=profile.__dict__.keys())
        df.to_csv(target_file, index=True)
    df = pd.read_csv(target_file, index_col=0)
    df = df.append(profile.__dict__, ignore_index=True)
    df.to_csv(target_file, index=True)

def make_data_folder_if_needed():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        os.chmod(DATA_FOLDER, 0o777)

def load_config():
    with open(os.path.join(os.path.dirname(__file__), 'network_mining_config.json')) as f:
        return json.load(f)

if __name__ == "__main__":
    print("\n\n----------- Script started -----------\n")
    print(" Welcome to the contacts crawler!\n")
    print(" The script will scroll through your LinkedIn contacts in Firefox\n")
    print(" And save the links to the actual profiles\n")
    print(" Please make sure you are logged in to LinkedIn in your Firefox\n")
    print(" Scraping parameters can be configured from 'network_mining_config.json'\n")
    print("\n--------------------------------------\n")
    print("Launching...\n")
    config = load_config()
    BATCH_SIZE = config["crawler_batch_size"]
    bookmark_file = os.path.join(DATA_FOLDER, config["crawler_bookmark_file_name"])
    target_data_file = os.path.join(DATA_FOLDER, config["crawler_result_file_name"])
    print("The output will be stored to: {}\n".format(target_data_file))

    make_data_folder_if_needed()
    browser = BrowserFactory.create()
    scraper = LinkedInProfileScraper(browser)
    bookmarkRepo = BookmarkRepo(bookmark_file)

    total = 0
    progress = 0
    try:
        print("Scrapping your next {} contacts".format(BATCH_SIZE))
        bookmark = bookmarkRepo.load_bookmark()
        scraper.go_to_my_connections()
        # totalConnections = scraper.scrape_contacts_number()
        # print("Bookmarked progress {} / {}\n".format(bookmark, totalConnections))
        
        total = config["crawler_my_contacts_limit"]
        print("Bookmarked progress {} / {} Connections".format(bookmark, total))
        time.sleep(5)

        print("\nScrolling to # {} ...\n".format(bookmark))

        # total = int(totalConnections.replace(' Connections', ''))

        for i in tqdm(range(bookmark, min(bookmark + BATCH_SIZE, total))):
            scraper.scroll_to_index(i)
            profile = scraper.scrape_short_profile(i)
            save_profile(profile, target_data_file)
            bookmarkRepo.save_bookmark(i)
            progress = i + 1

    except Exception as ex:
        print("----------- ERROR -----------")
        print(ex)
        traceback.print_exc()
    finally:
        browser.quit()
        print("\nSaved progress: {} / {}".format(progress, total))
        print("\n----------- Script finished -----------\n")