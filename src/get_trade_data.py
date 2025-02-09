import httpx
import json
import pandas as pd


def combine_url_with_params(url, params):
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



def get_data_census(year, month, export=True, CTY_NAME = None, NAICS = None):
    """
    Fetching trade data from the Census.
    Input:
        export: True-export, False-import
        year: 4-digit year
        month: 2-digit month
        CTY_NAME = country name
        NAICS = NAICS code
    Output:
        return json output
    """
    url = "https://api.census.gov/data/timeseries/intltrade"
    params = {"YEAR": year, "MONTH":month, "CTY_NAME":CTY_NAME, "NAICS":NAICS}
    
    if export:
        url = url+"/exports/statenaics"
        params["get"] = "CTY_CODE,CTY_NAME,NAICS,NAICS_LDESC,ALL_VAL_MO"
    else:
        url = url+"/imports/statenaics"
        params["get"] = "CTY_CODE,CTY_NAME,NAICS,NAICS_LDESC,GEN_VAL_MO"

    url_fetch = combine_url_with_params(url, params)
    
    response = httpx.get(url_fetch, timeout=30.0)

    response_data = {"headers": dict(response.headers),  # save header in dict
                     "body": response.json()}

    return json.dumps(response_data, indent=2)


def top_n_value(data, n, export = True):
    """
    Given the retrieved json data, return top N values.
    
    Input:
        data: json data
        n: the number of top values we get
        export: True-export, False-import
    Output:
        dataframe
    """
    json_data = json.loads(data)
    df = pd.DataFrame(json_data["body"][1:], columns = json_data["body"][0])
    
    value = "GEN_VAL_MO"
    if export:
        value = "ALL_VAL_MO"

    df[value] =  df[value].replace("-", 0)
    df[value] =  df[value].astype(int)
    return df.nlargest(n, value)
