import os.path
import json
import subprocess
import sys
from tqdm import tqdm
from random import uniform
import time

def load_config():
    with open(os.path.join(os.path.dirname(__file__), 'network_mining_config.json')) as f:
        return json.load(f)

if __name__ == "__main__":
    print("\n\n----- Scheduler script started -----\n")
    print(" Welcome to the emails scraper scheduler!\n")
    print(" The script will run emails scraper scirpt multiple times\n")
    print(" Scheduling and scraping parameters can be configured from 'network_mining_config.json'\n")
    print("\n--------------------------------------\n")
    print("Beginning the schedule...\n")

    config = load_config()
    number_of_runs = config["scheduler_number_of_scraper_runs"]
    delay_between_runs = config["scheduler_seconds_between_scraper_runs"]
    script_path = os.path.join(os.path.dirname(__file__), 'emails-linkedin-scraping-pipeline.py')

    for i in tqdm(range(0, number_of_runs)):
        print("===================>> Starting run #{}".format(i + 1))
        result = subprocess.run(["python3", script_path])
        if (not result.returncode == os.EX_OK):
            print("\n\n----------- ERROR in a Scheduled run  -----------\n")
            print(" Caution! Do not rerun the scheduler until:\n")
            print(" 1. You're sure you can access your LinkedIn account manually")
            print(" 2. You've successfully executed new 'emails-linkedin-scraping-pipeline.py' run\n")
            print(" Caution! Otherwise there is a risk of making too many wrong requests to LinkedIn and being banned\n")
            sys.exit(os.EX_DATAERR)
        if (not i + 1 == number_of_runs):
            t = uniform(1.23 + delay_between_runs, 9.9999 + delay_between_runs)
            print("Waiting for {} seconds between scraper runs...".format(t))
            time.sleep(t)
        
    print("\n----------- The Scheduled runs are all completed. -----------\n")
