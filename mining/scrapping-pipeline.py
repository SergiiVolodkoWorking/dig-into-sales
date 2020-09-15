import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInCompanyScrapper import LinkedInCompanyScrapper
import os.path

source_data_file = "./data/airtable-unique-companies.csv"
target_data_file = "./data/airtable-companies-with-linkedin-data.csv"
unreconized_companies_file = "./data/unrecognized-airtable-companies.csv"
bookmark_file = "./data/mining_airtable_bookmark.txt"

bulk_size = 10

# source_data_file = "./data/companies-from-deals.csv"
# target_data_file = "./data/companies-with-linkedin-data.csv"
# unreconized_companies_file = "./data/unrecognized-companies.csv"

def load_all_companies():
    return pd.read_csv(source_data_file, index_col=0)

def print_company(company, i):
    print('======================================')
    print('->', i)
    print(company["Associated Company"])
    print(company["Industry"])
    print(company["Employees"])
    print(company["HQ"])
    print(company["Website"]) 
    # print(company["Deal Name"])
    # print(company["Associated Company"])

def search_on_linkedin(browser, company):
    company_name = company["Associated Company"]
    search_url ='https://www.linkedin.com/search/results/companies/?keywords={}'.format(company_name)
    browser.get(search_url)

def save_to_unreconized(company):
    if not os.path.isfile(unreconized_companies_file):
        df = pd.DataFrame(company, columns=company.axes[0])
        df.to_csv(unreconized_companies_file, index=True)
    df = pd.read_csv(unreconized_companies_file, index_col=0)
    df = df.append(company)
    df.to_csv(unreconized_companies_file, index=True)

def save_bookmark(i):
    with open(bookmark_file, "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    with open(bookmark_file, "r") as file:
        return int(file.read())

def scrap_company(scrapper, company_id, company):
    url = "https://www.linkedin.com/company/{}/about/".format(company_id)
    description, size, specialties, established, industry, website, headquarter, logo_url = scrapper.get_company_data(url)
    company["LinkedIn description"] = description
    company["LinkedIn size"] = size
    company["LinkedIn specialties"] = specialties
    company["LinkedIn established"] = established
    company["LinkedIn id"] = company_id
    company["LinkedIn url"] = url
    company["LinkedIn Industry"] = industry
    company["LinkedIn website"] = website
    company["LinkedIn temporary logo"] = logo_url
    company["LinkedIn headquarter"] = headquarter
    return company

def save_found_company(company):
    if not os.path.isfile(target_data_file):
        df = pd.DataFrame(company, columns=company.axes[0])
        df.to_csv(target_data_file, index=True)
    df = pd.read_csv(target_data_file, index_col=0)
    df = df.append(company)
    df.to_csv(target_data_file, index=True)

if __name__ == "__main__":
    companies = load_all_companies()

    browser = BrowserFactory.create()
    scrapper = LinkedInCompanyScrapper(browser)

    bookmark = load_bookmark()
    print('Starting from:', bookmark)
    try:
        for i in range(bookmark, bookmark + bulk_size):
            company = companies.iloc[i]

            print_company(company, i)
            search_on_linkedin(browser, company)
            company_id = input('Enter company id: ')
            company_id = company_id.replace('/about', '').replace('/', '')

            if not company_id:
                print('skipping...')
                save_to_unreconized(company)
            else:
                print('fetching...')
                scrapped_company = scrap_company(scrapper, company_id, company)
                save_found_company(scrapped_company)
            save_bookmark(i)
    finally:
        browser.quit()
        print('The flow is completed.')