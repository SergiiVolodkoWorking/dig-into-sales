# Data Mining

## LinkedIn profiles mining

Process consist of two stages:
1. Scroll through all my contacts and store links (with `my-contacts-crawler.py`)
2. Iterate through stored links and scrape contact's and their current companies (with `emails-linkedin-scrapper-pipeline.py`)

### Installation - Mac

**1. Environment**

Scripts are scraping data via Firefox. To not mess up with your main browser. Make sure you have Firefox installed.

Make sure you have [Homebrew](https://brew.sh/). To install it execute in your terminal:

 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`

Then execute following commands from your terminal:

`brew install python`

`brew install geckodriver`

**2. Project setup**

Install python dependencies

Execute following commands in your terminal:

`pip3 install pandas`

`pip3 install selenium`

`pip3 install tqdm`

Clone the project
In terminal navigate to a folder where you want this project to be stored.
And execute: 
`git clone https://github.com/SergiiVolodkoWorking/dig-into-sales.git`

### Usage
Both crawling and scraping scripts are configured via [network_mining_config.json](network_mining_config.json) 

Before running scripts login to LinkedIn in your Firefox browser.


**Start crawling**

From `dig-into-sales/mining` folder execute:

`python3 my-contacts-crawler.py`


**Only after crawling Start scrapping**

From `dig-into-sales/mining` folder execute:

`python3 emails-linkedin-scrapping-pipeline.py`


**Result Data**

`dig-into-sales/data` folder will be created by the script and will contain bookmarks and the scrapped data