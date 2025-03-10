import pytest
from src.get_trade_data import (combine_url_with_params, 
                             url_to_cache_key, get_data_census)

def test_url_to_cache_key():
    url = "https://api.census.gov/data/timeseries/intltrade/imports/statenaics?get=CTY_CODE"
    result = url_to_cache_key(url)
    assert result == "api.census.gov_data_timeseries_intltrade_imports_statenaics_get=cty_code"
