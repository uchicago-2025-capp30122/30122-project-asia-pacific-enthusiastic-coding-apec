import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
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

def bygroup_get_trade_data(naics):
    """
    Get a trade data and make a pd.DataFrame grouped by year and country.
    Input:
        naics(str): 4-digit number of naics code
    Output:
        pd.DataFrame
    """
    
    all_df = []
    for year in range(2010, 2025):
        data = json.loads(get_trade_data.get_data_census(str(year), None, False, None, naics))
        df = pd.DataFrame(data["body"][1:], columns = data["body"][0])
        all_df.append(df)
    
    combined_df = pd.concat(all_df, ignore_index=True)
    combined_df["GEN_VAL_MO"] = combined_df["GEN_VAL_MO"].astype(float)

    # filtered year and country and calculate toal import values.
    return combined_df[combined_df["CTY_CODE"].str.match(r"-|[1-7]\d{3}")].groupby(
        ["YEAR", "CTY_NAME"])["GEN_VAL_MO"].sum().reset_index()


def find_production_value(naics):
    """
    Find a total amount of domestic production based on given naics
    Input:
        naics(str): 4-digit number of naics code
    Output:
        total amount of domestic production(float)
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
    df["NAIC 2017-4digits"] = df["NAIC 2017-4digits"].astype(str)

    return (df.loc[df["NAIC 2017-4digits"] == naics, "Production"].iloc[0]) * 1000

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.DEPENDENCY_GRAPH, "figure"),
        Input(ids.NAICS_DROPDOWN, "value"),
        )
    
    def get_data(naics):
        """
        make a line graph which indicates trend of import dependency.
        Input:
            naics(str): combination of 4-digit NAICS CODE and name of items
        Output:
        plotly.graph_objects.Figure(line graph)
        """
        naics_code = naics[:4]
        annual_imports = bygroup_get_trade_data(naics_code)
        production = find_production_value(naics_code)

        #Add a column of dependency and get top 3 countries of dependency
        annual_imports["dependency"] = annual_imports["GEN_VAL_MO"] / (production + annual_imports["GEN_VAL_MO"])        
        
        imports_sorted = annual_imports.loc[annual_imports["YEAR"]=="2024"].sort_values(by="GEN_VAL_MO", ascending=False)
        top3_country = imports_sorted.iloc[1:4]["CTY_NAME"].tolist()

        all_country = annual_imports[annual_imports["CTY_NAME"]=="TOTAL FOR ALL COUNTRIES"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=all_country["YEAR"],
            y=all_country["dependency"],
            mode = "lines + markers",
            name = "Total",
            line=dict(width=3)
        ))
        
        for country in top3_country:
            country_import = annual_imports[annual_imports["CTY_NAME"]==country]
            fig.add_trace(go.Scatter(
            x=country_import["YEAR"],
            y=country_import["dependency"],
            mode = "lines + markers",
            name = country,
            line=dict(width=1)
            ))

        fig.update_layout(
            title="Import dependency in total and top three countries",
            xaxis_title = "year",
            yaxis_title = "import dependency"
        )

        return fig





