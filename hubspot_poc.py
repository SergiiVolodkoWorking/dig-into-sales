from hubspot3 import Hubspot3
from hubspot3.companies import CompaniesClient
from hubspot3.contacts import ContactsClient

from hubspot3.oauth2 import OAuth2Client

API_KEY = ""

client_id=""
client_secret=""

code = ""

#client = Hubspot3(api_key=API_KEY)

if __name__ == "__main__":
    # # client = CompaniesClient(api_key=API_KEY)

    # # #client.create({'Name':"test"})

    # # for company in client.get_all():
    # #     print(company)


    # # hubspot3_client = Hubspot3(
    # #     access_token=access_token,
    # #     client_id=client_id,
    # #     client_secret=client_secret,
    # #     refresh_token=refresh_token,
    # #     oauth2_token_getter=oauth2_token_getter,
    # #     oauth2_token_setter=oauth2_token_setter,
    # # )



    tokens = OAuth2Client().get_tokens(
        authorization_code= code,
        redirect_uri= "http://localhost:8000",
        client_id=client_id,
        client_secret=client_secret
    )

    client = CompaniesClient(
        access_token = tokens['access_token'],
        refresh_token = tokens['refresh_token'],
        client_id=client_id,
        client_secret=client_secret)

    print(client.get_all())
