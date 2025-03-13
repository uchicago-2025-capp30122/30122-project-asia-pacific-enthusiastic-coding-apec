import pytest
import tempfile
import json
import pandas as pd
from pathlib import Path
from unittest.mock import patch, Mock
from src.get_data_prod_agri import (FetchException, get_data_agri)


def test_cached_get_error_response():
    with patch("httpx.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(FetchException):
            get_data_agri("https://quickstats.nass.usda.gov/api/api_GET/", "ABCD")


