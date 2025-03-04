import httpx
import csv

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
    #"state_alpha": "VA",
    "year":"2017"
}

url="https://quickstats.nass.usda.gov/api/api_GET/"


response = httpx.get(url, params=params)

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


agriculture_NAICS = "agriculture_NAICS.csv"
#   Writing in dictionary
with open(agriculture_NAICS, mode="w") as file:
    writer = csv.writer(file)
    # Headers
    writer.writerow(["NAICS", "Production"])
    # Value
    for key, value in dict_final.items():
        writer.writerow([key, value])

