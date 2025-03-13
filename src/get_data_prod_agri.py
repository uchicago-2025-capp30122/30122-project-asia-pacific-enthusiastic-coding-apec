import httpx
import csv
from pathlib import Path
import json
import time
import os



class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


CACHE_DIR = Path(__file__).parent / "_cache"
DATA_DIR = Path(__file__).parent / "data"


try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
       raise Exception(
       "For getting the agricultural production data, please provide "
       "an API_KEY. You can request one from https://quickstats.nass.usda.gov/api"
       "Last update: March-2025"
    )
    

# Parameters for the query
params = {
    "key": API_KEY,
    "source_desc": "CENSUS",
    "statisticcat_desc":"sales",
    "unit_desc": "$",
    "agg_level_desc": "NATIONAL",
    "domain_desc":"NAICS CLASSIFICATION",
    "year":"2022"
}

url="https://quickstats.nass.usda.gov/api/api_GET/"

def get_data_agri(url, params):
    
    time.sleep(0.5)

    response = httpx.get(url, params=params)
    if response.status_code == 200:

        response_data = {"headers": dict(response.headers), 
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

        agriculture_NAICS = DATA_DIR / "agriculture_NAICS.csv"
        DATA_DIR.mkdir(exist_ok=True)


        #   Writing in dictionary
        with open(agriculture_NAICS, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(["NAICS", "Production"])
        
            for key, value in dict_final.items():
                writer.writerow([key, value])

    raise FetchException(response)    
