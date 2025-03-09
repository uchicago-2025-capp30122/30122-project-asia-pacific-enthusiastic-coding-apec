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

PARENT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(PARENT_DIR))
import get_trade_data

# 0. Register as Dash page
dash.register_page(__name__, path="/descriptive",
                   title="Descriptive",
                   name="Descriptive")

# 1. App Layout

current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
start_year = 2010  # Start year for the slider
months = [(year, month) for year in range(
    start_year, current_year) for month in range(1, 13)]
month_labels = [f"{year}-{str(month).zfill(2)}" for year, month in months]

# Obtener valores únicos de NAICS_LDESC desde el DataFrame
NAICS_OPTION = (
 '1111: OILSEEDS AND GRAINS',
 '1112: VEGETABLES AND MELONS',
 '1113: FRUITS AND TREE NUTS',
 '1114: MUSHROOMS, NURSERY AND RELATED PRODUCTS',
 '1119: OTHER AGRICULTURAL PRODUCTS',
 '1121: CATTLE',
 '1122: SWINE',
 '1123: POULTRY AND EGGS',
 '1124: SHEEP, GOATS AND FINE ANIMAL HAIR',
 '1125: FARMED FISH AND RELATED PRODUCTS',
 '1129: OTHER ANIMALS',
 '1132: FORESTRY PRODUCTS',
 '1133: TIMBER AND LOGS',
 '1141: FISH, FRESH, CHILLED OR FROZEN AND OTHER MARINE PRODUCTS',
 '1151: CROPS & PRODUCTS SUPPORTING CROP PRODUCTION',
 '1152: SUPPORT ACTIVITIES FOR ANIMAL PRODUCTION',
 '2111: OIL AND GAS',
 '2121: COAL AND PETROLEUM GASES',
 '2122: METAL ORES',
 '2123: NONMETALLIC MINERALS',
 '3111: ANIMAL FOODS',
 '3112: GRAIN AND OILSEED MILLING PRODUCTS',
 '3113: SUGAR AND CONFECTIONERY PRODUCTS',
 '3114: FRUIT AND VEGETABLE PRESERVES AND SPECIALTY FOODS',
 '3115: DAIRY PRODUCTS',
 '3116: MEAT PRODUCTS AND MEAT PACKAGING PRODUCTS',
 '3117: SEAFOOD PRODUCTS PREPARED, CANNED AND PACKAGED',
 '3118: BAKERY AND TORTILLA PRODUCTS',
 '3119: FOODS, NESOI',
 '3121: BEVERAGES',
 '3122: TOBACCO PRODUCTS',
 '3131: FIBERS, YARNS, AND THREADS',
 '3132: FABRICS',
 '3133: FINISHED AND COATED TEXTILE FABRICS',
 '3141: TEXTILE FURNISHINGS',
 '3149: OTHER TEXTILE PRODUCTS',
 '3151: KNIT APPAREL',
 '3152: APPAREL',
 '3159: APPAREL ACCESSORIES',
 '3161: LEATHER AND HIDE TANNING',
 '3162: FOOTWEAR',
 '3169: OTHER LEATHER PRODUCTS',
 '3211: SAWMILL AND WOOD PRODUCTS',
 '3212: VENEER, PLYWOOD, AND ENGINEERED WOOD PRODUCTS',
 '3219: OTHER WOOD PRODUCTS',
 '3221: PULP, PAPER, AND PAPERBOARD MILL PRODUCTS',
 '3222: CONVERTED PAPER PRODUCTS',
 '3231: PRINTED MATTER AND RELATED PRODUCT, NESOI',
 '3241: PETROLEUM AND COAL PRODUCTS',
 '3251: BASIC CHEMICALS',
 '3252: RESIN, SYNTHETIC RUBBER, & ARTIFICIAL & SYNTHETIC FIBERS & FILIMENT',
 '3253: PESTICIDES, FERTILIZERS AND OTHER AGRICULTURAL CHEMICALS',
 '3254: PHARMACEUTICALS AND MEDICINES',
 '3255: PAINTS, COATINGS, AND ADHESIVES',
 '3256: SOAPS, CLEANING COMPOUNDS, AND TOILET PREPARATIONS',
 '3259: OTHER CHEMICAL PRODUCTS AND PREPARATIONS',
 '3261: PLASTICS PRODUCTS',
 '3262: RUBBER PRODUCTS',
 '3271: CLAY AND REFRACTORY PRODUCTS',
 '3272: GLASS AND GLASS PRODUCTS',
 '3273: CEMENT AND CONCRETE PRODUCTS',
 '3274: LIME AND GYPSUM PRODUCTS',
 '3279: OTHER NONMETALLIC MINERAL PRODUCTS',
 '3311: IRON AND STEEL AND FERROALLOY',
 '3312: STEEL PRODUCTS FROM PURCHASED STEEL',
 '3313: ALUMINA AND ALUMINUM AND PROCESSING',
 '3314: NONFERROUS METAL (EXCEPT ALUMINUM) AND PROCESSING',
 '3315: FOUNDRIES',
 '3321: CROWNS, CLOSURES, SEALS AND OTHER PACKING ACCESSORIES',
 '3322: CUTLERY AND HANDTOOLS',
 '3323: ARCHITECTURAL AND STRUCTURAL METALS',
 '3324: BOILERS, TANKS, AND SHIPPING CONTAINERS',
 '3325: HARDWARE',
 '3326: SPRINGS AND WIRE PRODUCTS',
 '3327: BOLTS, NUTS, SCREWS, RIVETS, WASHERS AND OTHER TURNED PRODUCTS',
 '3329: OTHER FABRICATED METAL PRODUCTS',
 '3331: AGRICULTURE AND CONSTRUCTION  MACHINERY',
 '3332: INDUSTRIAL MACHINERY',
 '3333: COMMERCIAL AND SERVICE INDUSTRY MACHINERY',
 '3334: VENTILATION, HEATING, AIR-CONDITIONING, AND COMMERCIAL REFRIGERATION EQUIPMENT',
 '3335: METALWORKING MACHINERY',
 '3336: ENGINES, TURBINES, AND POWER TRANSMISSION EQUIPMENT',
 '3339: OTHER GENERAL PURPOSE MACHINERY',
 '3341: COMPUTER EQUIPMENT',
 '3342: COMMUNICATIONS EQUIPMENT',
 '3343: AUDIO AND VIDEO EQUIPMENT',
 '3344: SEMICONDUCTORS AND OTHER ELECTRONIC COMPONENTS',
 '3345: NAVIGATIONAL, MEASURING, ELECTROMEDICAL, AND CONTROL INSTRUMENTS',
 '3346: MAGNETIC AND OPTICAL MEDIA',
 '3351: ELECTRIC LIGHTING EQUIPMENT',
 '3352: HOUSEHOLD APPLIANCES AND MISCELLANEOUS MACHINES, NESOI',
 '3353: ELECTRICAL EQUIPMENT',
 '3359: ELECTRICAL EQUIPMENT AND COMPONENTS, NESOI',
 '3361: MOTOR VEHICLES',
 '3362: MOTOR VEHICLE BODIES AND TRAILERS',
 '3363: MOTOR VEHICLE PARTS',
 '3364: AEROSPACE PRODUCTS AND PARTS',
 '3365: RAILROAD ROLLING STOCK',
 '3366: SHIPS AND BOATS',
 '3369: TRANSPORTATION EQUIPMENT, NESOI',
 '3371: HOUSEHOLD AND INSTITUTIONAL FURNITURE AND KITCHEN CABINETS',
 '3372: OFFICE FURNITURE (INCLUDING FIXTURES)',
 '3379: FURNITURE RELATED PRODUCTS, NESOI',
 '3391: MEDICAL EQUIPMENT AND SUPPLIES',
 '3399: MISCELLANEOUS MANUFACTURED COMMODITIES',
 '9100: WASTE AND SCRAP',
 '9300: USED OR SECOND-HAND MERCHANDISE',
 '9800: GOODS RETURNED TO CANADA (EXPORTS ONLY); U.S. GOODS RETURNED AND REIMPORTED ITEMS (IMPORTS ONLY)',
 '9900: OTHER SPECIAL CLASSIFICATION PROVISIONS'
)

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
            options=NAICS_OPTION,
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
        dcc.Graph(id=ids.MAP_IMPORT),
        dcc.Graph(id=ids.MAP_EXPORT),
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
    Output(ids.MAP_IMPORT, "figure"),
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

    fig = px.choropleth(data_import, locations="iso_alpha3",
                        color="USD",
                        # column to add to hover information
                        hover_name="CTY_NAME",
                        color_continuous_scale=px.colors.sequential.Viridis,
                        title=f"US Trade Imports ({naics}) - {selected_date}")
    # update layout
    fig.update_layout(
        height=700,
        title_x=0.5,
    )

    return fig


# 4. Interactive export controls


@callback(
    Output(ids.MAP_EXPORT, "figure"),
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

    fig = px.choropleth(data_export, locations="iso_alpha3",
                        color="USD",
                        # column to add to hover information
                        hover_name="CTY_NAME",
                        color_continuous_scale=px.colors.sequential.Viridis,
                        title=f"US Trade Exports ({naics}) - {selected_date}")
    # update layout
    fig.update_layout(
        height=700,
        title_x=0.5,
    )

    return fig
