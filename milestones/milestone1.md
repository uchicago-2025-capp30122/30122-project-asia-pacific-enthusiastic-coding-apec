# {Team Name}
APEC (Asia Pacific Enthusiastic Coding)

## Members

- Tina Du <tinawdu@uchicago.edu>
- Mauro Ttito <maurottito@uchicago.edu>
- Ryota Shimizu<ryotas@uchicago.edu>
- Jose Pajuelo <jpajuelo@uchicago.edu>


## Abstract

Built an program for visualizing the logistics flow of trade and domestic production of United States. The solution can visualize the logistics flow of trade and production by year and month, by country and by items.  This application would enable users to intuitively track the flow of specific items. For instance, users could explore questions such as: “From or to which country is these specific items imported or exported, and how does this compare to amount of domestic production?” or “What items are imported from or exported to this country?” These insights would be presented through visualizations like maps and graphs.
Additionally, incorporating domestic and international time-series data would allow for more advanced analyses. For example, users could identify trends in specific items whose trade volumes increase or decrease. They could also analyze highly trade-dependent items and their source countries.
The information would be extracted from online official webpages. This dataset would be analyzed, cleaned and transform in order to create adequate visualization tools for the solution.

## Preliminary Data Sources

### Data Source #1:  Census Bureau API: International Trade
This dataset provides information about US import and exports. The data comes from web page or API with the following URL https://usatrade.census.gov/.
To access to data is necessary to first login. We are not sure whether we can web-scrape from the API which requires login.

### Data Source #2:  Input-Output Accounts Data from Bureau of Economic Analysis
This dataset provides information about US domestic production. The data comes from web page with the following URL https://www.bea.gov/industry/input-output-accounts-data. The matrix is a little complexed so one of the challenges are getting proper information from this data.

Another potential problem is that Harmonized System code (HS code), which is use for classifying products in international trade is different from the North American Industry Classification System (NAICS), which is used in domestic data. So, combining these codes could be challenging. 


## Preliminary Project Plan


1.	Data exploration (Jose)
2.	Data ingestion (including web scraping) (Ryota & Mauro)
3.	Cleaning data (Tina)
4.	Combining different codes from two sources. (Ryota) 
5.	Operation and transformation of data (creation of indicators and others) (Jose & Tina)
6.	Visualization  (Ryota & Mauro)

You might also begin to think about who will work on what.
This can be very brief, and will almost certainly change by the next milestone.

## Questions

1.	 A similar program has been already made by another party.
( https://oec.world/en/profile/country/usa) Though we think we can differentiate our project by incorporating domestic data and trade data, we would like to know to what extent originality is required for our program in this project?

2.	Are Programs expected to function universally, even if the data on the web pages is updated in the future? For, HS codes, NAICS codes, and their correspondence may slightly change over the years, making it difficult to guarantee their strict validity for future data.

