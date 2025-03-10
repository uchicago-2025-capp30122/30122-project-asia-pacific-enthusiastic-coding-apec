from get_trade_data import get_data_census
import json
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os


def run_scatter(year, month):
    """
    Create a scatter graph of Herfindahl-Hirschman Index(Index of Import 
    concentration 0<HHI<=10000) on Import dependency.
    
    Input:
        year (str): 4-digit year
        month (str): 2-digit month
    Output:
        None(Create a png file)
    """

    data = json.loads(get_data_census(year, month, False, None, None))
    in_country = pd.DataFrame(data["body"][1:], columns = data["body"][0])

    # filter 4-digit NAICS code and create df with NAICS code and HHI
    hhi_by_naics = in_country[in_country["NAICS"].str.match(r"\d{4}")].groupby(
        ["NAICS", "NAICS_LDESC"]).apply(calculate_hhi).reset_index()
    
    #Add a column of domestic production
    hhi_production = add_production_data(hhi_by_naics)
    
    #Import dependency calculated as import/(production + import)
    hhi_production["Import_dp"] = hhi_production["total_import"] / (
        hhi_production["total_import"] + hhi_production["Production"])

    create_scatter(hhi_production, year, month)


def calculate_hhi(grouped_df: pd.DataFrame):
    """
    Calcurate HH Index from dataframe.
    Input:
        grouped_df: Datafreame grouped by NAICS code
    Output:
        pd.Series(HH Index, total amount of import)
    """
    total = int(grouped_df.loc[grouped_df["CTY_CODE"]=="-", 
                            "GEN_VAL_MO"].iloc[0])
    
    # choosing only countries(drop such as EU, NAFTA...)
    filtered_cty = grouped_df[grouped_df["CTY_CODE"].str.match(r"[1-7]\d{3}")]

    # HHI is calculated as s1^2 + s2^2 + ... where sn is the share percentage of
    # import from each country expressed as a whole number(0-100).
    filtered_cty["share"] = 100 * filtered_cty["GEN_VAL_MO"].astype(int)/total

    return pd.Series([(filtered_cty["share"] ** 2).sum(), total], 
                     index=["HHI", "total_import"])


def add_production_data(hhi_df: pd.DataFrame):
    """
    Add a column of domestic production to dataframe.
    Input:
        hhi_df: Datafreame
    Output:
        Dataframe with added production data.
    """

    if not os.path.exists("four_digits_NAICS.csv"):
        get_data_census("/2022/ecncomp?get=NAICS2017,RCPTOT&for=state:*")
    
    # Create a dic of {NAICS: production} to find values efficiently
    df = pd.read_csv("four_digits_NAICS.csv")
    production_dic = pd.Series(df["Production"].values * 1000, 
                        index = df["NAIC 2017-4digits"].astype(str)).to_dict()
    
    hhi_df["Production"] = hhi_df["NAICS"].apply(lambda key: 
                                                    production_dic.get(key, 0))
    
    return hhi_df


def create_scatter(hhi_pro_df: pd.DataFrame, year, month):
    """
    Plot a scatter graph.
    """
    
    filtered = hhi_pro_df[hhi_pro_df["Production"] != 0].reset_index()
    plt.scatter(filtered["Import_dp"], filtered["HHI"], 
                s=filtered["total_import"]/5000000, alpha=0.5)
    
    """
    for i, label in enumerate(filtered["NAICS_LDESC"]):
        plt.text(filtered["Import_dp"][i], filtered["HHI"][i], label, 
                 fontsize = 7, color = "black")
    """
    
    plt.xlabel("Import dependency(import / production + import)")
    plt.ylabel("Herfindahl-Hirschman Index")
    plt.title(f'HHI on Import Dependency({year}-{month})')
    plt.savefig("HHI_Import_dependency.png")
    plt.show


