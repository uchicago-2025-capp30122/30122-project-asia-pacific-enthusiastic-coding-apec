import pandas as pd
import pytest
from unittest.mock import patch, Mock

with patch("dash.register_page") as mock_register_page:
    from src.app.pages.hhi import calculate_hhi, add_production_data, get_data

@pytest.fixture
def sample_df():
    sample_data = [
    [
      "CTY_CODE",
      "NAICS_LDESC",
      "GEN_VAL_MO",
      "YEAR",
      "MONTH",
      "CTY_NAME",
      "NAICS"
    ],
    [
      "5200",
      "OILSEEDS AND GRAINS",
      "33890",
      "2021",
      "03",
      "UNITED ARAB EMIRATES",
      "1111"
    ],
    [
      "5210",
      "OILSEEDS AND GRAINS",
      "3240",
      "2021",
      "03",
      "YEMEN",
      "1111"
    ],
    [
      "5330",
      "OILSEEDS AND GRAINS",
      "10558999",
      "2021",
      "03",
      "INDIA",
      "1111"
    ],
    [
      "5350",
      "OILSEEDS AND GRAINS",
      "120720",
      "2021",
      "03",
      "PAKISTAN",
      "1111"
    ],
    [
      "5360",
      "OILSEEDS AND GRAINS",
      "12192",
      "2021",
      "03",
      "NEPAL",
      "1111"
    ],
    [
      "5380",
      "OILSEEDS AND GRAINS",
      "2508",
      "2021",
      "03",
      "BANGLADESH",
      "1111"
    ],
    [
      "5460",
      "OILSEEDS AND GRAINS",
      "1029796",
      "2021",
      "03",
      "BURMA",
      "1111"
    ],
    [
      "5490",
      "OILSEEDS AND GRAINS",
      "757286",
      "2021",
      "03",
      "THAILAND",
      "1111"
    ] ,
    [
      "-",
      "OILSEEDS AND GRAINS",
      "12518631",
      "2021",
      "03",
      "TOTAL FOR ALL COUNTRIES",
      "1111"
    ]]
    return pd.DataFrame(sample_data[1:], columns=sample_data[0])

def test_calculate_hhi(sample_df):
    result = calculate_hhi(sample_df)
    assert type(result) == pd.Series
    assert result.to_dict() == ""