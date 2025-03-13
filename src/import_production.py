import httpx
import json
import numpy as np
import csv

'''
This function extract data of table sale sof the economic census for the 2022 Year
agregate it by NAIC of 4 digits. It store the information in a csv file in a directory data.
Nevertheless, this information is not available anymore since goverment has started to quit some table from the web.


https://www.cnbc.com/2025/02/06/some-census-bureau-data-now-appears-to-be-unavailable-to-the-public.html

We used the previous stored csv for the rest of the application
'''
def get_data_census(param):
    """
       #api_code="/2022/ecncomp?get=group(EC2200COMP)&NAICS2017=pseudo(N0600.00)&YEAR=2022&ucgid=0100000US"
    """
    url = "https://api.census.gov/data"
    url_fetch = url+param
    response = httpx.get(url_fetch)

    response_data = {"headers": dict(response.headers),  # save header in dict
                     "body": response.json()
                     }

    data_stored={}
    for row in response_data["body"][1:]:
        data_stored[row[36]]=row[51]

###GETTING THE FULL NAICS
    full_NAICS = "full_NAICS_production.csv"

#   Writing in dictionary
    with open(full_NAICS, mode="w") as file:
        writer = csv.writer(file)
        # Headers
        writer.writerow(["NAIC 2017", "Production"])
        # Value
        for key, value in data_stored.items():
            writer.writerow([key, value])


###For 4 digit format
    four_digit_NAIC=set()
    for element in data_stored.keys():
        four_digit_NAIC.add(element[:4])

    data_4digits={}
    
    for NAIC in four_digit_NAIC:
        data_4digits[NAIC]=0

    for key, value in data_stored.items():
        if data_4digits[key[:4]]>=0:
            data_4digits[key[:4]]=data_4digits[key[:4]]+float(data_stored[key])


    fourdigits_NAICS = "four_digits_NAICS.csv"

#   Writing in dictionary
    with open(fourdigits_NAICS, mode="w") as file:
        writer = csv.writer(file)
        # Headers
        writer.writerow(["NAIC 2017-4digits", "Production"])
        # Value
        for key, value in data_4digits.items():
            writer.writerow([key, value])
