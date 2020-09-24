# Data Mining

## LinkedIn profiles mining

Process consist of two stages:
1. Scroll through my network and store the links (using `my-contacts-crawler.py`)
2. Iterate through stored links and scrape every contact + their current company data (using `emails-linkedin-scrapper-pipeline.py`)

Make sure you have Firefox installed. The scripts are scraping data using Firefox to not mess up with your main browser. 

### [Experimental] Automatic Installation - Mac

Clone the project
In terminal navigate to a folder where you want this project to be stored.
And execute: 

`git clone https://github.com/SergiiVolodkoWorking/dig-into-sales.git`

In terminal navigate inside the cloned folder (`cd dig-into-sales`)

There execute: `chmod 755 ./setup_mining.sh`

Then execute: `./setup_mining.sh`

### Manual Installation - Mac
The same process but in manual steps

**1. Environment**

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

`dig-into-sales/data` folder will be created by the scripts and will contain bookmarks and the scrapped data