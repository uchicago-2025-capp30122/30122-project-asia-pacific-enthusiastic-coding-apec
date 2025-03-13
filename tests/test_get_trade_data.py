import pytest
import tempfile
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, Mock
from src.get_trade_data import (FetchException, combine_url_with_params, 
                             url_to_cache_key, get_data_census)

def test_combine_url_with_params():
    result = combine_url_with_params("https://example.com/api/", {"api_key": "abc", "page": 2})
    assert result == "https://example.com/api/?api_key=abc&page=2"

def test_url_to_cache_key():
    url = "https://api.census.gov/data/timeseries/intltrade/imports/statenaics?get=CTY_CODE"
    result = url_to_cache_key(url)
    assert result == "api.census.gov_data_timeseries_intltrade_imports_statenaics_get=cty_code"

@pytest.fixture
def temp_cache_dir():
    """Fixture to create a temporary cache directory."""
    with tempfile.TemporaryDirectory() as tempdirname:
        temp_dir = Path(tempdirname)
        with patch("src.get_trade_data.CACHE_DIR", temp_dir):
            yield temp_dir

def test_get_data_census_new_request(temp_cache_dir):
    with patch("httpx.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = [("key_1", "value_1"), ("key_2", "value_2")]
        response_content = [["response_column"], ["response_body"]]
        mock_response.json.return_value = response_content
        mock_get.return_value = mock_response

        # first request makes a call
        result = json.loads(get_data_census("2021", "03"))
        df = pd.DataFrame(result["body"][1:], columns=result["body"][0])
        value = df["response_column"].iloc[0]

        assert value == "response_body"
        mock_get.assert_called_once()

        # and is written to cache
        url = "https://api.census.gov/data/timeseries/intltrade/exports/statenaics"
        params = {"YEAR": "2021", "MONTH":"03", "CTY_NAME":None, "NAICS":None, "get": "CTY_CODE,NAICS_LDESC,ALL_VAL_MO"}
        url_fetch = combine_url_with_params(url, params)
        cache_key = url_to_cache_key(url_fetch)

        assert (temp_cache_dir / cache_key).exists(), (
            f"No file exists at {temp_cache_dir / cache_key}. "
        )


def test_get_data_census_cached_request(temp_cache_dir):
    # First, create a cache entry
    url = "https://api.census.gov/data/timeseries/intltrade/imports/statenaics"
    params = {"YEAR": "2022", "MONTH":"03", "CTY_NAME":None, "NAICS":None, "get": "CTY_CODE,NAICS_LDESC,GEN_VAL_MO"}
    url_fetch = combine_url_with_params(url, params)
    cache_key = url_to_cache_key(url_fetch)

    cache_file = temp_cache_dir / cache_key
    cache_file.write_text("cached content")

    # ensure that our code used the cache and did not hit the URL
    with patch("httpx.get") as mock_get:
        result = get_data_census("2022", "03", False, None, None)

        assert result == "cached content"
        mock_get.assert_not_called()


def test_cached_get_error_response(temp_cache_dir):
    with patch("httpx.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(FetchException):
            get_data_census("2021", "03")
