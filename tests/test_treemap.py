import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
from src.app.pages.treemap import get_iso_alpha3, get_continent


def test_get_iso_alpha3():
    assert get_iso_alpha3("United States") == "USA"
    assert get_iso_alpha3("China") == "CHN"
    assert get_iso_alpha3("Unknownland") is None

def test_get_continent():
    assert get_continent(100) == "NORTH AMERICA"
    assert get_continent(400) == "EUROPE"
    assert get_continent(999) == "UNKNOWN"

if __name__ == "__main__":
    test_get_iso_alpha3()
    test_get_continent()
    print("All tests passed!")
