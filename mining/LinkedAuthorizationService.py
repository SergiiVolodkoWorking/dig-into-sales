from linkedin_v2 import linkedin
### !important 
### pip3 install python-linkedin
### pip3 install --upgrade https://github.com/ozgur/python-linkedin/tarball/master
from time import sleep
from BrowserFactory import BrowserFactory
from selenium.webdriver.common.by import By

class LinkedAuthorizationService:
    browser = {}

    def __init__(self, auth_browser):
        self.browser = auth_browser

    def refresh_token(self, api_key, api_secret, linkedin_email, linkedin_pass):
        print("Refreshing the token...")
        RETURN_URL = "https://localhost:8000"

        authentication = linkedin.LinkedInAuthentication(api_key, api_secret, RETURN_URL, ['w_share'])
        print("Navigating to authorization url")
        self.browser.get(authentication.authorization_url)
        sleep(2)
        #raw_input("Please allow access manually and press Enter to continue...")
        print("Logging in")
        self.perform_login(linkedin_email, linkedin_pass)

        print("Extracting code")
        url = self.browser.current_url
        start = 'code='
        end = '&state='
        code = url[url.find(start)+len(start):url.find(end)]
        authentication.authorization_code = code
        print("Getting the token")
        return authentication.get_access_token()

    def perform_login(self, linkedin_email, linkedin_pass):
        if(self.is_submit_page()):
            print("Fast login")
            try:
                self.browser.find_element_by_id("oauth__auth-form__submit-btn").click()
            except:
                pass
        else:
            print("Proper login")
            self.browser.find_element_by_name("session_key").clear()
            self.browser.find_element_by_name("session_key").send_keys(linkedin_email)
            self.browser.find_element_by_name("session_password").send_keys(linkedin_pass)
            
            print("Submitting form")
            sleep(1)
            try:
                self.browser.find_element_by_xpath('//button[text()="Sign in"]').click()          
                if(self.is_submit_page()):
                    self.browser.find_element_by_id("oauth__auth-form__submit-btn").click()
            except:
                pass

    def is_submit_page(self):
        sleep(2)
        submit_buttons = self.browser.find_elements(By.XPATH, "//button[@id='oauth__auth-form__submit-btn']")
        print("Submit buttons :", len(submit_buttons))
        return len(submit_buttons) > 0

if __name__ == "__main__":
    browser = BrowserFactory.create()

    auth = LinkedAuthorizationService(browser)

    token = auth.refresh_token('api_key', 'api_secret', 'linkedin_email', 'linkedin_pass')

    print(token)
    browser.quit()