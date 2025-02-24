# Visualization of trade data in the US

## Abstract

This package is built for extracting online information on trade and production in the United States from the Economic Census (https://www.census.gov). After processing the data, an interactive graphic dashboard will be displayed. This dashboard will provide helpful insights about the main traded products, including their destination and origin.

For this milestone, we achieved the following:

• Trade data extracted and cleaned
• Production data partially extracted and cleaned, ready for interact with Trade Data
• Initial mockup of the dashboard

## Prerequisites

For using this package, is necessary to run uv sync for downloading the necessary libraries.

## Structure

All the python files are located in the folder "src". The structure of the package and the python files associated are the following:

### a. For downloading and processing the data

• src/get_trade_data.py: This file contains the function get_data_census and other helper functions to extract and clean the trade data from the Census. The output of this function is a JSON string.

• src/import_production.py: This file contains the function get_data_census to extract and clean the production data from the Census and prepare it for integration with the trade data. The output of this function is a CSV file. This does not include data from agricultural goods, which need to be extracted differently from the input/output table.

### b. For constructing indexs and graphics
• src/hhi_production.py: This file builds the Herfindahl-Hirschman Index, which measures market concentration to determine which city produces the most in the US. This index will be used in the dashboard.

• src/main.py: This file runs the code located in src/components and displays the dashboard. It is activated by running uv run src/__main__.py. Note that this dashboard is a mock with no real data.

## Next steps
The next steps for the final presentation are:

• Work on cleaning the production data. This means achieving the same code structure as for the trade data and including the agricultural production data.
• Develop pytest tests for the functions that require them.
• Use the real data for the dashboard.
• Present the final version of the dashboard.
