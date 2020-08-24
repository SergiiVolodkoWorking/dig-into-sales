import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInScrapper import LinkedInScrapper

source_data_file = "./data/companies-with-linkedin-data-and-aggregated-findep-industry-and-directors.csv"
target_data_file = "./data/companies-with-extended-linkedin-data-and-aggregated-findep-industry-and-directors.csv"
bookmark_file = "./data/enrich_scrapped_bookmark.txt"

def save_bookmark(i):
    with open(bookmark_file, "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    with open(bookmark_file, "r") as file:
        return int(file.read())

def print_company(company):
    print(company["Associated Company"])
    print(company["LinkedIn headquarter"])
    print(company["LinkedIn website"])
    print(company["LinkedIn site favicon"])
    print(company["LinkedIn temporary logo"])

def load_companies():
    return pd.read_csv(source_data_file, index_col=0)

def save_company(company):
    df = pd.read_csv(target_data_file, index_col=0)
    df = df.append(company)
    df.to_csv(target_data_file, index=True)

def scrap_company(scrapper, company):
    url = company["LinkedIn url"]
    c = scrapper.get_company_data(url)
    company["LinkedIn website"] = c.website
    company["LinkedIn temporary logo"] = c.logo_url
    company["LinkedIn headquarter"] = c.headquarter
    return company

if __name__ == "__main__":
    companies = load_companies()

    browser = BrowserFactory.create()
    scrapper = LinkedInScrapper(browser)

    bulk_size = 50
    bookmark = load_bookmark()
    print('Starting from:', bookmark)
    try:
        for i in range(bookmark, bookmark + bulk_size):
            company = companies.iloc[i]

            print('======================================')
            print('fetching... ->', i)
            print(company["LinkedIn url"])

            if(pd.isnull(company["LinkedIn url"])):
                save_company(company)
                print('Skipped.')
            else:
                scrapped_company = scrap_company(scrapper, company)
                save_company(scrapped_company)
                print_company(scrapped_company)
            
            save_bookmark(i)
    finally:
        browser.quit()
        print('The flow is completed.')