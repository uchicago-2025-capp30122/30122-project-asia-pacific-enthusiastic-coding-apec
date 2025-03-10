import dash
import plotly.express as px
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import datetime
from . import ids
import sys
from pathlib import Path
import json
import pandas as pd
import pycountry
import numpy as np

PARENT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(PARENT_DIR))
import get_trade_data

continent_mapping = {
    "1": "NORTH AMERICA",
    "2": "CENTRAL AMERICA",
    "3": "SOUTH AMERICA",
    "4": "EUROPE",
    "5": "ASIA",
    "6": "AUSTRALIA AND OCEANIA",
    "7": "AFRICA"
}

# Function to determine continent from CTY_CODE
def get_continent(cty_code):
    prefix = str(cty_code)[0]  # Extract the first digit
    return continent_mapping.get(prefix, "UNKNOWN")

# 0. Register as Dash page
dash.register_page(__name__, path="/treemap",
                   title="Treemap",
                   name="Treemap")

# 1. App Layout

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
start_year = 2010  # Start year for the slider
months = [(year, month) for year in range(
    start_year, current_year) for month in range(1, 13)]
month_labels = [f"{year}-{str(month).zfill(2)}" for year, month in months]

layout = html.Div(
    [
        html.H4("US Trade Export and Import"),
        html.P(
            "In these graphs, we show the visual change in export and import "
            "data through time."
            ),
        html.P(
            "NAICS: North American Industry Classification System"
            ),
        html.P(
            "You can select any NAICS code and description and date "
            "(year - month) from the date slider"
            ),
        # Input for interactive map
        html.Label("NAICS:"),
        dcc.Dropdown(
            id=ids.NAICS_DROPDOWN,
            options=ids.NAICS_OPTION,
            value='1111: OILSEEDS AND GRAINS',
            multi=False,
        ),
        html.Label("Select Year and Month:"),
        dcc.Slider(
            id=ids.DATE_SLIDER,
            min=0,
            max=len(month_labels) - 1,
            value=len(month_labels) - 12,  # Default current year - 1
            marks={i: label for i, label in enumerate(
                month_labels) if "-01" in label},
            step=1,
        ),
        # Callout to map
        dcc.Graph(id=ids.TREE_MAP_IMPORT),
        dcc.Graph(id=ids.TREE_MAP_EXPORT),
        html.Div(
            id="foot_note_map",
            children=[
                html.Ol(
                    id="foot_note_map_list",
                    children=[
                        html.Li([
                            "Units in USA dollars."
                            ]),
                        html.Li(
                            "Import and export data is sourced from the "
                            "United States Census Bureau."
                        ),
                    ],
                )
            ],
        ),
    ]
)


# 2. Get iso alpha3 map codes
def get_iso_alpha3(country_name):
    """
    Convert country name to ISO Alpha-3 code
    """
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None

# 3. Interactive import controls


@callback(
    Output(ids.TREE_MAP_IMPORT, "figure"),
    Input(ids.NAICS_DROPDOWN, "value"),
    Input(ids.DATE_SLIDER, "value"),
    )
def get_data_import(naics, date_index):
    """
    Create a map graph of Imports from USA.

    Input:
        naics: North American Industry Classification System
        date_index:
            year (str): 4-digit year
            month (str): 2-digit month
    Output:
        None(Create a map figure)
    """
    # Get naics
    naics_code = naics[:4]

    # Get year and month
    selected_date = month_labels[date_index]
    year, month = selected_date.split("-")

    # import
    import_census = json.loads(
        get_trade_data.get_data_census(year, month, False, None, naics_code))
    data_import = pd.DataFrame(
        import_census["body"][1:], columns=import_census["body"][0])

    # Convert country names (CTY_NAME) to ISO Alpha-3 codes
    data_import["iso_alpha3"] = data_import["CTY_NAME"].apply(get_iso_alpha3)

    # Drop rows where ISO Alpha-3 conversion failed
    data_import = data_import.dropna(subset=["iso_alpha3"])

    # val in numeric and replace NaN with 0
    data_import["USD"] = pd.to_numeric(data_import["GEN_VAL_MO"],
                                       errors="coerce")
    data_import["USD"] = data_import["USD"].fillna(0)

    data_import["continent"] = data_import["CTY_CODE"].apply(get_continent)


    midpoint_value = np.average(data_import['USD'], weights=data_import['USD'])

    fig = px.treemap(data_import, path=[px.Constant("world"), 'continent', 'CTY_NAME'],
                     color='USD',
                     values = "USD",
                     hover_data=['iso_alpha3'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=midpoint_value
                     )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    
    return fig



# 4. Interactive export controls

@callback(
    Output(ids.TREE_MAP_EXPORT, "figure"),
    Input(ids.NAICS_DROPDOWN, "value"),
    Input(ids.DATE_SLIDER, "value"),
    )
def get_data_export(naics, date_index):
    """
    Create a map graph of Export from USA.

    Input:
        naics: North American Industry Classification System
        date_index:
            year (str): 4-digit year
            month (str): 2-digit month
    Output:
        None(Create a map figure)
    """
    # Get naics
    naics_code = naics[:4]

    # Get year and month
    selected_date = month_labels[date_index]
    year, month = selected_date.split("-")

    # import
    import_census = json.loads(
        get_trade_data.get_data_census(year, month, True, None, naics_code))
    data_export = pd.DataFrame(
        import_census["body"][1:], columns=import_census["body"][0])

    # Convert country names (CTY_NAME) to ISO Alpha-3 codes
    data_export["iso_alpha3"] = data_export["CTY_NAME"].apply(get_iso_alpha3)

    # Drop rows where ISO Alpha-3 conversion failed
    data_export = data_export.dropna(subset=["iso_alpha3"])

    # val in numeric and replace NaN with 0
    data_export["USD"] = pd.to_numeric(data_export["ALL_VAL_MO"],
                                       errors="coerce")
    data_export["USD"] = data_export["USD"].fillna(0)

    data_export["continent"] = data_export["CTY_CODE"].apply(get_continent)

    midpoint_value = np.average(data_export['USD'], weights=data_export['USD'])

    fig = px.treemap(data_export, path=[px.Constant("world"), 'continent', 'CTY_NAME'],
                     color='USD',
                     values = "USD",
                     hover_data=['iso_alpha3'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=midpoint_value
                     )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    
    return fig
