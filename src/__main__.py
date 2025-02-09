import sys
from request_api_census import get_data_census

get_data_census("/timeseries/intltradeimports/naics?get=E_COMMODITY_SDESC,CTY_NAME,ALL_VAL_YR,DIST_NAME,E_COMMODITY_SDESC&time=2013-24-1&key=a4790051a25236cfca83e83b4957639b278298d2")

if __name__ == "__main__":
    main()
