# 1. Abstract

This package is built for extracting online information on trade and production in the United States from the Economic Census (https://www.census.gov). After processing the data, an interactive graphic dashboard will be displayed. This dashboard will provide helpful insights about the main traded products, including their destination and origin.

For this milestone, we achieved the following:

• Trade data extracted and cleaned
• Production data partially extracted and cleaned, ready for interact with Trade Data
• Initial mockup of the dashboard

# 2. Members

- Tina Dou <tdou@uchicago.edu>
- Mauro Ttito <maurottito@uchicago.edu>
- Ryota Shimizu<ryotas@uchicago.edu>
- Jose Pajuelo <jpajuelo@uchicago.edu>


# 3. Data Sources

We extracted from the Economic Census (https://www.census.gov), trough the use of its API. There are two databases we extracted from the Census:

• Data of  Trade: The code for extracted this data is located in src/get_trade_data.py This file contains the function get_data_census and other helper functions to extract and clean the trade data from the Census. The output of this function is a JSON string.

• Data of  Production: The code for extracted this data is located insrc/import_production.py: This file contains the function get_data_census to extract and clean the production data from the Census and prepare it for integration with the trade data. The output of this function is a CSV file. This does not include data from agricultural goods, which need to be extracted differently from the input/output table.

# 4. How to Run

For using this package, is necessary to run uv sync for downloading the necessary libraries.
All the python files are located in the folder "src". 

• For getting the dashboard we should run uv run src/__main__.py. Note that this dashboard is a mock with no real data.

• There is also an additional python file (src/hhi_production.py). This file builds the Herfindahl-Hirschman Index, which measures market concentration to determine which city produces the most in the US. This index will be used in the dashboard.

# 5. Next steps

The next steps for the final presentation are:

• Work on cleaning the production data. This means achieving the same code structure as for the trade data and including the agricultural production data.
• Develop pytest tests for the functions that require them.
• Use the real data for the dashboard.
• Present the final version of the dashboard.
