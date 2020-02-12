from linkedin_v2 import linkedin
from time import sleep
import random
import urllib

class LinkedInRepository:

    application = {}

    def __init__(self, linkedin_application):
        self.application = linkedin_application

    def find_company_by_name(self, company_name):
        sleep(random.random() / 3)
        selectors=[{'companies': ['id']}]
        response = self.search_company(params={'baseSearchParams.keywords': company_name})
        print(response)
        if response['companies']['_total'] == 0:
            return None
        companies = response['companies']['values']

        return None if len(companies)<0 else companies[0]

    
    def search_company(self, params):
        url = '%s/search?q=companiesV2&%s' % (
            'https://api.linkedin.com/v2', urllib.parse.urlencode(params))
        response = self.application.make_request('GET', url)
        # raise_for_error(response)
        return response.json()


if __name__ == "__main__":
    from BrowserFactory import BrowserFactory
    from LinkedAuthorizationService import LinkedAuthorizationService
    browser = BrowserFactory.create()

    try:
        linkedin_email = "linkedin_email"
        linkedin_pass = "linkedin_pass"
        api_key = "api_key"
        api_secret = "api_secret"
        token = LinkedAuthorizationService(browser).refresh_token(api_key, api_secret, linkedin_email, linkedin_pass)
        print('token', token)
        application = linkedin.LinkedInApplication(token=token)
        repo = LinkedInRepository(application)
        print(repo.find_company_by_name("Microsoft"))
    finally:
        browser.quit()