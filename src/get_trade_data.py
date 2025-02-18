import httpx
import json
import pandas as pd


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


def get_data_census(year: str, month: str, export: bool = True, 
                    CTY_NAME: str = None, NAICS: str = None):
    """
    Fetching trade data from the Census.
    Input:
        year (str): 4-digit year
        month (str): 2-digit month
        export (bool): True-export, False-import
        CTY_NAME = country name
        NAICS = NAICS code

    Return:
        return json output
    """
    url = "https://api.census.gov/data/timeseries/intltrade"
    params = {"YEAR": year, "MONTH":month, "CTY_NAME":CTY_NAME, "NAICS":NAICS}
    
    if export:
        url = url+"/exports/statenaics"
        params["get"] = "CTY_CODE,NAICS_LDESC,ALL_VAL_MO"  # ,CTY_NAME,NAICS
    else:
        url = url+"/imports/statenaics"
        params["get"] = "CTY_CODE,NAICS_LDESC,GEN_VAL_MO"  # ,CTY_NAME,NAICS

    url_fetch = combine_url_with_params(url, params)
    print(url_fetch)
    response = httpx.get(url_fetch, timeout=30.0)
    response_data = {"headers": dict(response.headers),  # save header in dict
                     "body": response.json()}

    return json.dumps(response_data, indent=2)


def top_n_value(data: str, n: int, export: bool = True):
    """
    Given the retrieved json data, return top N values.
    
    Input:
        data (str): json data
        n (int): the number of top values we get
        export (bool): True-export, False-import
    
    Return:
        pd.dataframe: DataFrame with top n values
    """
    json_data = json.loads(data)
    df = pd.DataFrame(json_data["body"][1:], columns = json_data["body"][0])
        
    value = "ALL_VAL_MO" if export else "GEN_VAL_MO"  # export - import

    df[value] =  df[value].replace("-", 0)
    df[value] =  df[value].astype(int)
    return df.nlargest(n, value)


# ipython3 example
# data = src.get_trade_data.get_data_census("2022", "09")  # export=True, CTY_NAME = None, NAICS = None
# src.get_trade_data.top_n_value(data, 8, True)