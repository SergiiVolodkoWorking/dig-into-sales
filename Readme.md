# Data Mining

## LinkedIn profiles mining

Process consist of two stages:
1. Scroll through my network and store the links (using `my-contacts-crawler.py`)
2. Iterate through stored links and scrape every contact + their current company data (using `emails-linkedin-scraping-pipeline.py`)

### Crucial preconditions
The scripts are scraping data using Firefox to not mess up with your main browser.

Please Make sure you:
1. have Firefox installed.
2. then logged to LinkedIn with Firefox and checked `Remember Me` checkbox.
3. on successful login closed Firefox browser

### Automatic Installation - Mac

1. Setup developer tools
In your terminal execute:

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`

2. Clone the project
In terminal navigate to a folder where you want this project to be stored.
And execute: 

`git clone https://github.com/SergiiVolodkoWorking/dig-into-sales.git`

3. Execute setup script
In terminal navigate inside the cloned folder (`cd dig-into-sales`)

There execute: `chmod 755 ./setup_mining.sh`

Then execute: `./setup_mining.sh`

### Usage
Both crawling and scraping scripts are configured via [network_mining_config.json](network_mining_config.json) 

Before running scripts login to LinkedIn in your Firefox browser.


**Start crawling**

From `dig-into-sales/mining` folder execute:

`python3 my-contacts-crawler.py`


**Only after crawling Start scrapping**

From `dig-into-sales/mining` folder execute:

`python3 emails-linkedin-scraping-pipeline.py`


**Experimental: Scheduler to run emails scraper script multiple times**
When you're confident running scraping script and want to scrape more in one go.

From `dig-into-sales/mining` folder execute:

`python3 emails-linkedin-scraping-scheduler.py`

Note: like this there is a higher risk of making too many wrong requests to LinkedIn

**Result Data**

`dig-into-sales/data` folder will be created by the scripts and will contain bookmarks and the scrapped data