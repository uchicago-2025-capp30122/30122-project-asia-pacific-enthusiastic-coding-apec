import httpx
import json
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


    #get_data_census("/2022/ecncomp?get=NAICS2017,RCPTOT") ##Domestic production
    """
    url = "https://api.census.gov/data"
    url_fetch = url+param
    response = httpx.get(url_fetch, timeout=30.0)

    # for key, val in response.headers.items():
    #    print(f"   {key}: {val}")
    #    print("Body (start):", repr(response.text))

    response_data = {"headers": dict(response.headers),  # save header in dict
                     "body": response.json()
                     }
    #
    with open("data_extracted.json","w") as f:       
        json.dump(response_data, f, indent=2)
    
    #print(response_data)