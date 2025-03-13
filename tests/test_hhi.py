import pandas as pd
import pytest
from unittest.mock import patch

with patch("dash.register_page") as mock_register_page:
    from src.app.pages.hhi import calculate_hhi, add_production_data

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
    assert result.to_dict() == {'HHI': 7219.570490011338, 'total_import': 12518631.0}

def test_add_production_data(sample_df):
    result = add_production_data(sample_df)
    expected = {
        'CTY_CODE': {0: '5200', 1: '5210', 2: '5330', 3: '5350', 4: '5360', 
                     5: '5380', 6: '5460', 7: '5490', 8: '-'}, 
        'NAICS_LDESC': {0: 'OILSEEDS AND GRAINS', 1: 'OILSEEDS AND GRAINS', 
                        2: 'OILSEEDS AND GRAINS', 3: 'OILSEEDS AND GRAINS', 
                        4: 'OILSEEDS AND GRAINS', 5: 'OILSEEDS AND GRAINS', 
                        6: 'OILSEEDS AND GRAINS', 7: 'OILSEEDS AND GRAINS', 
                        8: 'OILSEEDS AND GRAINS'}, 
        'GEN_VAL_MO': {0: '33890', 1: '3240', 2: '10558999', 3: '120720', 
                       4: '12192', 5: '2508', 6: '1029796', 7: '757286', 
                       8: '12518631'},
        'YEAR': {0: '2021', 1: '2021', 2: '2021', 3: '2021', 4: '2021', 
                 5: '2021', 6: '2021', 7: '2021', 8: '2021'},
        'MONTH': {0: '03', 1: '03', 2: '03', 3: '03', 4: '03', 5: '03', 
                  6: '03', 7: '03', 8: '03'},
        'CTY_NAME': {0: 'UNITED ARAB EMIRATES', 1: 'YEMEN', 2: 'INDIA',
                     3: 'PAKISTAN', 4: 'NEPAL', 5: 'BANGLADESH', 6: 'BURMA',
                     7: 'THAILAND', 8: 'TOTAL FOR ALL COUNTRIES'},
        'NAICS': {0: '1111', 1: '1111', 2: '1111', 3: '1111', 4: '1111', 
                  5: '1111', 6: '1111', 7: '1111', 8: '1111'},
        'Production': {0: 625326666666.6666, 1: 625326666666.6666, 
                       2: 625326666666.6666, 3: 625326666666.6666, 
                       4: 625326666666.6666, 5: 625326666666.6666, 
                       6: 625326666666.6666, 7: 625326666666.6666, 
                       8: 625326666666.6666}}
    assert result.to_dict() == expected

