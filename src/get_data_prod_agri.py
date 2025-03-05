import httpx
import csv
from src.get_trade_data import FetchException, combine_url_with_params, url_to_cache_key
from pathlib import Path
import json
import time


CACHE_DIR = Path(__file__).parent / "_cache"
DATA_DIR = Path(__file__).parent / "data"

# Tu API key de NASS
api_key = "42C4EE11-6E45-31EC-8B5E-ACFFEA269143"

# Base URL for the API
#base_url = "https://quickstats.nass.usda.gov/api/api_GET/"

# Parameters for the query
params = {
    "key": api_key,
    "source_desc": "CENSUS",
    "statisticcat_desc":"sales",
    "unit_desc": "$",
    "agg_level_desc": "NATIONAL",
    "domain_desc":"NAICS CLASSIFICATION",
    "year":"2022"
}

url="https://quickstats.nass.usda.gov/api/api_GET/"

def get_data_agri(url, params):
    
    #CACHE_DIR.mkdir(exist_ok=True)
    #url_fetch = combine_url_with_params(url, params)
    #cache_key = url_to_cache_key(url_fetch)
    ##print(CACHE_DIR)
    #cache_file = CACHE_DIR/cache_key
    #print(cache_file)
    ## If there is a cache, return it. Otherwise send a request.
    #if cache_file.exists():
    #    with open (cache_file, "r") as f:
    #        return json.dumps(json.load(f))

    time.sleep(0.5)

    #response = httpx.get(url_fetch, timeout=30.0)
    response = httpx.get(url, params=params)

    if response.status_code == 200:

        response_data = {"headers": dict(response.headers),  # save header in dict
                            "body": response.json()
                            }

        data=response_data["body"]["data"]
        dict_final={}
        for row in data:
            NAICS_row=row['domaincat_desc']
            
            if len(NAICS_row)==28:
                start = NAICS_row.find('(') + 1 
                end = NAICS_row.find(')')  

                NAICS = NAICS_row[start:end]
                
                dict_final[NAICS]=row['Value']

        #agriculture_NAICS = "agriculture_NAICS.csv"
        agriculture_NAICS = DATA_DIR / "agriculture_NAICS.csv"
        DATA_DIR.mkdir(exist_ok=True)


        #   Writing in dictionary
        with open(agriculture_NAICS, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["NAICS", "Production"])
            # Value
            for key, value in dict_final.items():
                writer.writerow([key, value])

    #raise FetchException(response)
    
