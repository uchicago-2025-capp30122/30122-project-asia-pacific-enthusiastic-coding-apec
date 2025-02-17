import httpx
import json
import numpy as np
import csv

'''
try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    raise Exception(
        "Make sure that you have set the API Key environment variable as "
        "described in the README."
    )
DEFAULT_ARGS = {"api_key": API_KEY, "format": "json", "limit": "100"}


February 6 (Tina&Jose):
The ouput of the function get_data_cesus was change
now dont print but create a json file


'''
# Info from https://www.census.gov/data/developers/data-sets/international-trade.html

#response = httpx.get(
#    "https://api.census.gov/data/timeseries/intltrade/exports/hs?get=E_COMMODITY_SDESC,CTY_NAME,ALL_VAL_YR,DIST_NAME&time=2013-01&key=a4790051a25236cfca83e83b4957639b278298d2")


def get_data_census(param):
    """
    # TO DO: description of function
    # param eg: use this in ipython3
    # get_data_census("/timeseries/intltrade/exports/hs?get=E_COMMODITY_SDESC,CTY_NAME,ALL_VAL_YR,DIST_NAME&time=2013-01&CTY_CODE=1220")
    # get_data_census("/timeseries/intltrade/exports/hs?get=E_COMMODITY_SDESC,CTY_NAME,ALL_VAL_YR,DIST_NAME,E_COMMODITY_SDESC&time=2013-01&key=a4790051a25236cfca83e83b4957639b278298d2")
    # get_data_census("/timeseries/intltrade/exports/statehsexport?get=group(IT00EXPORTSTATEHS)&E_COMMODITY=-&time=2024-10&US_STATE=*&ucgid=W0100Y1WO")


    #get_data_census("/2022/ecncomp?get=NAICS2017,RCPTOT&for=state:*") ##Domestic production
    #api_code="/2022/ecncomp?get=group(EC2200COMP)&NAICS2017=pseudo(N0600.00)&YEAR=2022&ucgid=0100000US"
    """
    url = "https://api.census.gov/data"
    url_fetch = url+param
    response = httpx.get(url_fetch)
    #print("hello")

    # for key, val in response.headers.items():
    #    print(f"   {key}: {val}")
    #    print("Body (start):", repr(response.text))

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


###GETTING THE FULL NAICS
    fourdigits_NAICS = "four_digits_NAICS.csv"

#   Writing in dictionary
    with open(fourdigits_NAICS, mode="w") as file:
        writer = csv.writer(file)
        # Headers
        writer.writerow(["NAIC 2017-4digits", "Production"])
        # Value
        for key, value in data_4digits.items():
            writer.writerow([key, value])
