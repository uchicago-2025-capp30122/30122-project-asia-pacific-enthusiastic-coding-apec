import httpx
import json
import pandas as pd
from pathlib import Path
import re
import time
import datetime

CACHE_DIR = Path(__file__).parent / "_cache"
DATA_DIR = Path(__file__).parent / "data"

class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


def combine_url_with_params(url: str, params: dict):
    """
    Use httpx.URL to create a URL joined to its parameters, suitable for use
    for cache keys.

    Parameters:
        - url: a URL with or without parameters already
        - params: a dictionary of parameters to add

    Returns:
        The URL with parameters added, for example:

        >>> combine_url_with_params(
            "https://example.com/api/",
            {"api_key": "abc", "page": 2}
        )
        "https://example.com/api/?api_key=abc&page=2"
    """

    url = httpx.URL(url)
    params = dict(url.params) | params  # merge the dictionaries
    return str(url.copy_with(params=params))


def url_to_cache_key(url: str) -> str:
    """
    Convert a URL to a cache key that can be stored on disk.

    1) All keys would be lower case.
    2) The leading http(s):// would be removed.
    3) The remaining characters would all be specific characters.
       Any other characters would be converted to `_`.
    """
    removed_http = re.sub(r"https?://", "", url.lower())
    return re.sub(r"[^abcdefghijklmnopqrstuvwxyz1234567890%+,\^=._]", "_", 
                  removed_http )



def get_data_census(year: str, month: str, export: bool = True, 
                    CTY_NAME: str = None, NAICS: str = None):
    """
    Fetching trade data from the Census. This function also caches all GET 
    requests it makes, by writing the successful responses to disk.
    Input:
        year (str): 4-digit year
        month (str): 2-digit month
        export (bool): True-export, False-import
        CTY_NAME = country name
        NAICS = NAICS code

    Return:
        return json output
    """
    assert len(year) == 4, "year should be 4-digit number"
    if month is not None:
        assert len(month) == 2, "month should be 2-digit number"
    assert type(export) == bool, "export dummy should be bool"
    
    CACHE_DIR.mkdir(exist_ok=True)

    url = "https://api.census.gov/data/timeseries/intltrade"
    params = {"YEAR": year, "MONTH":month, "CTY_NAME":CTY_NAME, "NAICS":NAICS}
    
    if export:
        url = url+"/exports/statenaics"
        params["get"] = "CTY_CODE,NAICS_LDESC,ALL_VAL_MO"  # ,CTY_NAME,NAICS
    else:
        url = url+"/imports/statenaics"
        params["get"] = "CTY_CODE,NAICS_LDESC,GEN_VAL_MO"  # ,CTY_NAME,NAICS


    url_fetch = combine_url_with_params(url, params)
    cache_key = url_to_cache_key(url_fetch)
    cache_file = CACHE_DIR/cache_key

    # If there is a cache, return it. Otherwise send a request.
    if cache_file.exists():
        with open (cache_file, "r") as f:
            return f.read()

    time.sleep(0.5)
    response = httpx.get(url_fetch, timeout=30.0)

    if response.status_code == 200:
        response_data = {"headers": dict(response.headers),  # save header in dict
                        "body": response.json()}
        with open(cache_file, "w") as f:
            json.dump(response_data, f, indent=2)

        return json.dumps(response_data, indent=2)
    raise FetchException(response)