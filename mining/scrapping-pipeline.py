import pandas as pd
from BrowserFactory import BrowserFactory
from LinkedInScrapper import LinkedInScrapper

def load_all_companies():
    return pd.read_csv("./data/companies-from-deals.csv", index_col=0)

def print_company(company, i):
    print('======================================')
    print('->', i)
    print(company["Industry"])
    print(company["Deal Name"])
    print(company["Associated Company"])

def search_on_linkedin(browser, company):
    company_name = company["Associated Company"]
    search_url ='https://www.linkedin.com/search/results/companies/?keywords={}'.format(company_name)
    browser.get(search_url)

def save_to_unreconized(company):
    df = pd.read_csv("./data/unrecognized-companies.csv", index_col=0)
    df = df.append(company)
    df.to_csv('./data/unrecognized-companies.csv', index=True)

def save_bookmark(i):
    with open("./data/mining_bookmark.txt", "w") as text_file:
        text_file.write("{}".format(i+1))

def load_bookmark():
    with open("./data/mining_bookmark.txt", "r") as file:
        return int(file.read())

def scrap_company(scrapper, company_id, company):
    url = "https://www.linkedin.com/company/{}/about/".format(company_id)
    description, size, specialties, established, industry = scrapper.get_company_data(url)
    company["LinkedIn description"] = description
    company["LinkedIn size"] = size
    company["LinkedIn specialties"] = specialties
    company["LinkedIn established"] = established
    company["LinkedIn id"] = company_id
    company["LinkedIn url"] = url
    company["LinkedIn Industry"] = industry
    return company

def save_found_company(company):
    df = pd.read_csv("./data/companies-with-linkedin-data.csv", index_col=0)
    df = df.append(company)
    df.to_csv('./data/companies-with-linkedin-data.csv', index=True)

if __name__ == "__main__":
    companies = load_all_companies()

    browser = BrowserFactory.create()
    scrapper = LinkedInScrapper(browser)

    bulk_size = 25
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