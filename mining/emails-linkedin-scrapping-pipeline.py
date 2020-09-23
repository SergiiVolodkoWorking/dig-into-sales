import os.path
import pandas as pd
from BrowserFactory import BrowserFactory
from BookmarkRepo import BookmarkRepo
from LinkedInProfileScrapper import LinkedInProfileScrapper
from LinkedInCompanyScrapper import LinkedInCompanyScrapper
import time
import json
import traceback
from tqdm import tqdm

root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FOLDER = os.path.join(root_folder, "data")

def load_config():
    with open(os.path.join(os.path.dirname(__file__), 'network_mining_config.json')) as f:
        return json.load(f)

# def go_back(browser):
#     time.sleep(3)
#     browser.execute_script("window.history.go(-1)")
#     time.sleep(3)

def load_profile_links(config):
    source_file = os.path.join(DATA_FOLDER, config["crawler_result_file_name"])
    if not os.path.isfile(source_file):
        raise Exception("crawler_result_file_name is not found by path:\n {}".format(source_file))
    return pd.read_csv(source_file, index_col=0)

if __name__ == "__main__":
    print("\n\n----------- Script started -----------\n")
    print(" Welcome to the emails scrapper!\n")
    print(" The script will use links generated by the crawler\n")
    print(" It will visit LinkedIn profile and current company of every stored contact\n")
    print(" Please make sure you are logged in to LinkedIn in your Firefox\n")
    print(" Scraping parameters can be configured in 'network_mining_config.json'\n")
    print("\n--------------------------------------\n")
    print("Launching...\n")

    config = load_config()
    BATCH_SIZE = config["scrapper_batch_size"]
    bookmark_file = os.path.join(DATA_FOLDER, config["scrapper_bookmark_file_name"])
    target_data_file = os.path.join(DATA_FOLDER, config["scrapper_result_file_name"])

    browser = BrowserFactory.create()
    profileScrapper = LinkedInProfileScrapper(browser)
    companyScrapper = LinkedInCompanyScrapper(browser)
    bookmarkRepo = BookmarkRepo(bookmark_file)

    try:
        print("Visiting and scrapping your next {} contacts".format(BATCH_SIZE))
        bookmark = bookmarkRepo.load_bookmark()

        profile_links = load_profile_links(config)

        total = len(profile_links)

        print("Bookmarked progress {} / {}\n".format(bookmark, total))
        
        for i in tqdm(range(bookmark, min(bookmark + BATCH_SIZE, total))):
            url = profile_links.iloc[i]["link"]
            profile = profileScrapper.scrap_contact_info(url)
            if('/company/' in profile.company_link or
               '/school/' in profile.company_link):
               company_url = profile.company_link + 'about'
               company = companyScrapper.get_company_data(company_url)
            

    except Exception as ex:
        print("----------- ERROR -----------")
        print(ex)
        traceback.print_exc()
    finally:
        browser.quit()
        print("\n----------- Script finished -----------\n")
