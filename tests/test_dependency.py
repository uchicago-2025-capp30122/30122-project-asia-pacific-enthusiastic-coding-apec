import pandas as pd
import pytest
from unittest.mock import patch

with patch("dash.register_page") as mock_register_page:
    from src.app.pages.dependency import bygroup_get_trade_data, find_production_value


def test_bygroup_get_trade_data():
    result = bygroup_get_trade_data("1111")

    head_5 = {'YEAR': {0: '2010', 1: '2010', 2: '2010', 3: '2010', 4: '2010'},
              'CTY_NAME': {0: 'AFGHANISTAN', 1: 'ARGENTINA', 2: 'AUSTRALIA',
                           3: 'AUSTRIA', 4: 'BANGLADESH'},
                'GEN_VAL_MO': {0: 3140.0, 1: 51429414.0, 2: 6852143.0, 
                               3: 518693.0, 4: 24230.0}}
    assert result.head(5).to_dict() == head_5

def test_find_prodution_value():
    result = find_production_value("1111")
    assert result == 7503920000000.0


