import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import datetime
from . import ids
import sys
from pathlib import Path
import json
import pandas as pd
import os

PARENT_DIR = Path(__file__).parent.parent
sys.path.append(str(PARENT_DIR))
import get_trade_data
import import_production
from get_data_prod_agri import get_data_agri, api_key, url, params



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
    if not os.path.exists(PARENT_DIR / "data/four_digits_NAICS.csv"):
        import_production.get_data_census(
            "/2022/ecncomp?get=NAICS2017,RCPTOT&for=state:*")
    
    if not os.path.exists(PARENT_DIR / "data/agriculture_NAICS.csv"):
        get_data_agri(url, params)
    
    # Create a dic of {NAICS: production} to find values efficiently
    df_pro = pd.read_csv(PARENT_DIR / "data/four_digits_NAICS.csv")
    df_agri = pd.read_csv(PARENT_DIR / "data/agriculture_NAICS.csv")
    df_agri = df_agri.rename(columns = {"NAICS": "NAIC 2017-4digits"})
    df_agri["Production"] = df_agri["Production"].str.replace(
                                                        ",", "").astype(float)
    df = pd.concat([df_pro, df_agri], ignore_index=True)

    production_dic = pd.Series(df["Production"].values * 1000, 
                        index = df["NAIC 2017-4digits"].astype(str)).to_dict()
    
    hhi_df["Production"] = hhi_df["NAICS"].apply(lambda key: 
                                                    production_dic.get(key, 0))
    
    return hhi_df

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.HHINDEX_CHART, "figure"),
        Input(ids.YEAR_DROPDOWN, "value"),
        Input(ids.MONTH_DROPDOWN, "value"),
        )
    
    def get_data(year, month):
        """
        Create a scatter graph of Herfindahl-Hirschman Index(Index of Import 
        concentration 0<HHI<=10000) on Import dependency.
        
        Input:
            year (str): 4-digit year
            month (str): 2-digit month
        Output:
            None(Create a png file)
        """
        data = json.loads(
            get_trade_data.get_data_census(year, month, False, None, None))
        in_country = pd.DataFrame(data["body"][1:], columns = data["body"][0])

        # filter 4-digit NAICS code and create df with NAICS code and HHI
        hhi_by_naics = in_country[in_country["NAICS"].str.match(r"\d{4}")].groupby(
            ["NAICS", "NAICS_LDESC"]).apply(calculate_hhi).reset_index()
        
        #Add a column of domestic production
        hhi_production = add_production_data(hhi_by_naics)
        
        #Import dependency calculated as import/(production + import)
        hhi_production["Import_dp"] = hhi_production["total_import"] / (
            hhi_production["total_import"] + hhi_production["Production"])

        filtered = hhi_production[
            hhi_production["Production"] != 0
            ].reset_index()
        
        fig = px.scatter(
            filtered, x="Import_dp", y="HHI", 
            size=filtered["total_import"] / 5000000, 
            hover_name="NAICS_LDESC", size_max=60, opacity=0.5
            )
        
        return fig
        #return html.Div([dcc.Graph(figure=fig)], id=ids.HHINDEX_CHART)





