import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInScrapper import LinkedInScrapper
import os.path
import time

data_folder = "./data"

source_data_file = os.path.join(data_folder, 'hubspot-companies-with-linkedin-link.csv')
target_data_file = os.path.join(data_folder, 'hubspot-companies-with-linkedin-link-mined-data.csv')
bookmark_file = os.path.join(data_folder, 'mining_hubspot_with_linkedin_link_bookmark.txt')
bulk_size = 25

def save_bookmark(i):
    with open(bookmark_file, "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    with open(bookmark_file, "r") as file:
        return int(file.read())

def print_company(company):
    print(company["Company Name"])
    print(company["LinkedIn Name"])
    print(company["LinkedIn link"])
    print(company["LinkedIn url"])
    print(company["LinkedIn headquarter"])

def load_companies():
    return pd.read_csv(source_data_file, index_col=0)

def save_company(company):
    if not os.path.isfile(target_data_file):
        df = pd.DataFrame(company, columns=company.axes[0])
        df.to_csv(target_data_file, index=True)
    df = pd.read_csv(target_data_file, index_col=0)
    df = df.append(company)
    df.to_csv(target_data_file, index=True)

def scrap_company(scrapper, company):
    url = os.path.join(company["LinkedIn link"], "about")
    c = scrapper.get_company_data(url)
    company["LinkedIn description"] = c.description
    company["LinkedIn size"] = c.size
    company["LinkedIn specialties"] = c.specialties
    company["LinkedIn established"] = c.established
    company["LinkedIn url"] = url
    company["LinkedIn Industry"] = c.industry
    company["LinkedIn website"] = c.website
    company["LinkedIn temporary logo"] = c.logo_url
    company["LinkedIn headquarter"] = c.headquarter
    company["LinkedIn id"] = c.linkedin_id
    company["LinkedIn Name"] = c.linkedin_name

    return company

if __name__ == "__main__":
    companies = load_companies()

    browser = BrowserFactory.create()
    scrapper = LinkedInScrapper(browser)

    bookmark = load_bookmark()
    print('Starting from:', bookmark)
    try:
        for i in range(bookmark, bookmark + bulk_size):
            company = companies.iloc[i].copy()

            print('======================================')
            print('fetching... ->', i)

            if(pd.isnull(company["LinkedIn link"])):
                save_company(company)
                print('Skipped.')
            else:
                scrapped_company = scrap_company(scrapper, company)
                if(company["LinkedIn id"]=='unavailable'):
                    print('Unavailable - Skipped.')
                    continue
                save_company(scrapped_company)
                print_company(scrapped_company)
            
            save_bookmark(i)
            time.sleep(1)
    finally:
        browser.quit()
        print('The flow is completed.')