# 1. Abstract

This project investigates the economic impact of newly imposed tariffs and potential vulnerabilities in U.S. trade dependencies. Specifically, it addresses two key questions: 
- (1) How do recent tariffs affect specific products and trading partners?
- (2) Are there sectors where the U.S. is highly dependent on a small number of countries, posing economic risks?
To analyze these issues, we developed an analytical dashboard integrating trade and production data with economic modeling. Using the North American Industry Classification System (NAICS), our study examines trade flows, production concentration, and supply chain resilience. The findings provide insights into the composition of U.S. imports and exports, highlighting sectors susceptible to supply disruptions. This research offers valuable information for policymakers and industry leaders seeking to enhance economic stability and trade policy effectiveness.

[Short explanatory video](https://youtu.be/QslegtG212E)
# 2. Members

- Tina Dou <tdou@uchicago.edu>
- Mauro Ttito <maurottito@uchicago.edu>
- Ryota Shimizu<ryotas@uchicago.edu>
- Jose Pajuelo <jpajuelo@uchicago.edu>


# 3. Data Sources

These are the list of data which we use. We combine these data using NAICS codes as keys, allowing us to analyze and visualize them. Note that the trade data are monthly, whereas the domestic production data are for the year 2022.
- Census Bureau API: International Trade
This dataset provides information about US import and exports. The data comes from API international trade(https://api.census.gov/data).
We can retrieve monthly trade data by 4-digit NAICS(109 codes in total) code and country. (https://www.census.gov/data/developers/data-sets/economic-census.html)
- Census Bureau API: 2022 Economic Census
This dataset provides information about US domestic production. Census Bureau API: 2022 Economic Census. This data is updated every five years, so this program uses the most recent data available, 2022.We can retrieve domestic production data based on 4-digit NAICS code by country. Note that while it was accessible as of February 2024, it is no longer accessible as of March 2024 (https://www.cnbc.com/2025/02/06/some-census-bureau-data-now-appears-to-be-unavailable-to-the-public.html) . However, a necessary csv files is stored in the directory and can be used.
- USDA National Agricultural Statistics Service, Quick Stats AP
The Census Bureau API: 2022 Economic Census, has no information about agricultural items, so it was extracted from the USDA National Agricultural Statistics Service, which counts with an API service. The API key is requested from the page (https://www.nass.usda.gov/). The data corresponds to 2024.
- Other data for simulation:
The classification of countries by income level was obtained from the World Bank (https://blogs.worldbank.org/en/opendata/world-bank-country-classifications-by-income-level-for-2024-2025).  And the elasticity by type of product and level of income was obtained from Seale, Sergmi and Bernstein (2003): “International Evidence on Food Consumption Patterns” (https://ers.usda.gov/sites/default/files/_laserfiche/publications/47429/14755_tb1904_1_.pdf?v=56020) . We used the own-price slutsky elasticity, stored in a csv file.

# 4. How to Run

The software cleans and fetches the data, then passes that information to a Dash application to visualize on your local machine. The software has six pages with visualizations: 
- i home page; 
- ii descriptive page with export and import world maps; 
- iii descriptive page with export and import tree maps, 
- iv simulation page about some hypothetical tariffs, 
- v dependency page with an import tendency trend; and 
- vi Herfindahl–Hirschman index.
The software can be run from a machine with Python installed. We describe in details on how to run the software on your local machine:
Clone the Trade and Production Data in the United States Github Repository to your local machine terminal by running 
git clone git@github.com:uchicago-2025-capp30122/30122-project-asia-pacific-enthusiastic-coding-apec.git
Run “uv sync”
Put the API_KEY for agriculture data (https://quickstats.nass.usda.gov/api)
On Linux/MacOS:
-export API_KEY="str"
On Windows:
-$env:API_KEY = "str"
Run “uv run src/app/app.py” to start the dash. The first time this is going to take between 5 to 10 minutes depending on your computer and internet connection.

# 5. Application Structure

Directory and Module Breakdown
1. src/
This is the main source directory containing all the essential code for the project.
- app/: The core application module responsible for running the analytical dashboard.
- app.py: The main entry point for the dashboard application.
- pages/: A subdirectory containing different analysis and visualization components.
- dependency.py: Analyzes trade dependencies.
- descriptive.py: Provides descriptive statistics and summary reports.
- hhi.py: Computes the Herfindahl-Hirschman Index (HHI) for trade concentration.
- home.py: The landing page of the dashboard.
- ids.py: Handles data identifiers and mapping.
- simulation.py: Runs simulations on trade impact.
- treemap.py: Generates treemap visualizations of trade data.
- data/: Stores raw and processed datasets, extraction scripts, and trade-related computations.
agriculture_NAICS.csv, full_NAICS_production.csv, four_digits_NAICS.csv: Contain industry classification and production data.
data_extracted.json: Stores extracted trade data for analysis.
HHI_Import_dependency.png: A visualization related to trade dependencies.
Scripts:
- extract_trade_simulation.py: Extracts and processes trade simulation data.
- get_data_prod_agri.py: Retrieves agricultural production data.
- get_trade_data.py: Collects and structures trade data.
- hhi_production.py: Computes HHI for production concentration.
- import_production.py: Handles import-related production calculations.
- request_api_census.py: Fetches trade data from the U.S. Census API.
- time_dropdown.py: Manages time-based dropdown selections for visualization.

2. tests/
Contains unit tests to ensure the correctness of the implementation.
- test_dependency.py: Tests trade dependency analysis.
- test_get_prod_agri.py: Verifies agricultural production data retrieval.
- test_get_trade_data.py: Checks the correctness of trade data processing.
- test_hhi.py: Ensures correct computation of the Herfindahl-Hirschman Index.
- test_treemap.py: Validates the treemap visualization module.

3. Configuration & Setup Files
- .gitignore: Specifies files to be ignored by Git.
- .python-version: Specifies the Python version (3.13.1 in this case).
- pyproject.toml: Defines project dependencies and configurations.
- pytest.ini: Configures the pytest framework.
- README.md: Provides an overview and instructions for the project.
- uv.lock: Stores dependency versions for package management.

