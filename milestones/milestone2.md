# {APEC (Asia Pacific Enthusiastic Coding)} 

## Abstract 

Built a program for visualizing the logistics flow of trade and domestic production of United States. The solution can visualize the logistics flow of trade and production by year and month, by country and by items.  This application would enable users to intuitively track the flow of specific items. For instance, users could explore questions such as: “From or to which country is these specific items imported or exported, and how does this compare to amount of domestic production?” or “What items are imported from or exported to this country?” These insights would be presented through visualizations like maps and graphs. 

Additionally, incorporating domestic and international time-series data would allow for more advanced analyses. For example, users could identify trends in specific items whose trade volumes increase or decrease. They could also analyze highly trade-dependent items and their source countries. 

The information would be extracted from online official webpages. This dataset would be analyzed, cleaned and transform in order to create adequate visualization tools for the solution. 

## Data Sources 

### Data Reconciliation Plan 

We got two Data Sources in our project:  

### Data Source #1:  Census Bureau API: International Trade 

This dataset provides information about US import and exports. The data comes from web page with the following URL https://usatrade.census.gov/. 

This page has an API for exploring data. We have already got the API key for it. The next steps for extracting information are complete a code that retrieves data by choosing specific country, item(code), and year. 

In each data set (monthly or annually), the number of rows is supposed to be around 17,000(when using 10-digit HTS code) or 5,000(when using 6-digit HS code). And each rows have its export destination country or import origin country (about 200 countries). When running this program, it is expected to select one country or one item, and time. The unique key for connection is HTS(HS) code and we are interested in one variable, “imports(exports) in total value”. 

The information about exports and imports in this dataset uses the Harmonized System code (HS code). 

### Data Source #2:  Input-Output Accounts Data from Bureau of Economic Analysis 

This dataset provides information about US domestic production. The data comes from web page with the following URL https://www.bea.gov/industry/input-output-accounts-data.  

We already have downloaded the information of some tables which is stored in xlsx files. We got detailed information about the production in USA. This information is for 402 type of production gods and services, and has 423 columns which represent the use in other industries in the USA. Nevertheless, we are just interested in one variable, named “total commodity output(T007)” (1 column) The unique key variable for connection is 6-digit NAICS code. These data are provided in XLSX files, so we plan to pre-download it and refer to this data (without accessing it through our program). 

The information about production in this dataset uses the North American Industry Classification System (NAICS). 

### About get together the two datasets: 

The main problem for put the two datasets together is that both uses different code systems. Exploring related initiatives, we found projects that match NAICS and HS systems (https://www.census.gov/foreign-trade/schedules/b/2022/exp-code.txt). Even this is not a one-to-one match, is detailed enough for our goals. The main challenge here is to make this equivalence for the years which we are working with.   

## Project Plan 

1.  Data ingestion, through web scrapping and API management (Mauro & Tina) 
    Date expected: Week 5 
2.  Data cleaning (Jose & Tina) 
    Date expected: Week 6                 
4.  Combining different codes from two sources. (Ryota)  
    Date expected: Week 7 
5.  Operation and transformation of data (creation of indicators and others) (Jose & Tina) 
    Date expected: Week 7 (Draft version) - Week 9 (Final version) 
6.  Visualization (Ryota & Mauro) 
    Date expected: 7 (Draft version) - Week 9 (Final version) 

## Questions 

1.  We understand that our programs should be public. So, is there no problem if this program requires users to acquire their own API key to retrieve information from a government website? (Actually, we could get this API immediately.) 
2. If one of source data (data 2) is provided by xlsx file, can we download all of them in advance and incorporate it in our program (Don’t we need access this data through program)? 