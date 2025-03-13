import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as pxc
import pandas as pd
import json
from . import ids
from pathlib import Path
import csv
import sys
#import pycountry


COUNTRIES=['AFGHANISTAN', 'ALBANIA', 'ALGERIA', 'ANDORRA', 'ANGOLA',  'ARGENTINA', 'ARMENIA', 'ARUBA', 
               'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN', 'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 'BELARUS', 'BELGIUM', 
               'BELIZE', 'BENIN', 'BERMUDA', 'BHUTAN', 'BOLIVIA', 'BOTSWANA', 'BRAZIL',  'BRUNEI', 
               'BULGARIA', 'BURKINA FASO', 'BURUNDI', 'CABO VERDE', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAYMAN ISLANDS', 
               'CHAD', 'CHILE', 'CHINA', 'COLOMBIA','COMOROS',  'COSTA RICA', 'CROATIA', 
               'CUBA', 'CURACAO', 'CYPRUS', 'CZECH REPUBLIC', 'DENMARK', 'DJIBOUTI', 'DOMINICA', 'ECUADOR', 
               'EGYPT', 'EL SALVADOR', 'ESTONIA', 'ESWATINI', 'ETHIOPIA', 
               'FAROE ISLANDS', 'FINLAND', 'FRANCE',  'GABON',  'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GIBRALTAR', 'GREECE', 'GREENLAND', 'GRENADA', 'GUATEMALA', 'GUINEA', 'GUINEA-BISSAU',
                'GUYANA', 'HAITI', 'HONDURAS', 'HONG KONG', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN', 'IRAQ', 'IRELAND', 'ISRAEL', 'ITALY', 'JAMAICA', 
                'JAPAN', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KIRIBATI', 'KOREA, SOUTH', 'KOSOVO', 'KUWAIT',  'LAOS', 'LATVIA', 'LEBANON', 'LESOTHO', 
                'LIBERIA', 'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MACAU', 'MACEDONIA', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES', 'MALI', 'MALTA', 
                'MEXICO', 'MICRONESIA', 'MOLDOVA', 'MONACO', 'MONGOLIA', 'MONTENEGRO', 
                'MOROCCO', 'MOZAMBIQUE', 'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS', 'NEW CALEDONIA', 'NEW ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA',   
                'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU', 'PANAMA',  'PARAGUAY', 'PERU', 'PHILIPPINES',  'POLAND', 'PORTUGAL', 
                'QATAR', 'ROMANIA', 'RUSSIA', 'RWANDA', 'SAMOA', 'SAN MARINO', 'SAUDI ARABIA', 'SENEGAL', 'SERBIA', 'SEYCHELLES', 
                'SIERRA LEONE', 'SINGAPORE', 'SLOVAKIA', 'SLOVENIA', 'SOMALIA', 'SOUTH AFRICA', 'SOUTH SUDAN', 'SPAIN', 'SRI LANKA',
                'SUDAN', 'SURINAME', 'SWEDEN', 'SWITZERLAND', 'SYRIA', 'TAIWAN', 'TAJIKISTAN', 'TANZANIA', 'THAILAND', 'TIMOR-LESTE',
                'TOGO',  'TONGA',  'TUNISIA', 'TURKEY', 'TURKMENISTAN',  'UGANDA', 
                'UKRAINE', 'UNITED KINGDOM', 'URUGUAY', 'UZBEKISTAN',  'VENEZUELA', 'VIETNAM', 
                'YEMEN', 'ZAMBIA', 'ZIMBABWE']


PARENT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(PARENT_DIR))
#import get_trade_data
#import extract_trade_simulation

# 0. Register as Dash page
dash.register_page(__name__, path="/simulation",
                   title="Simulation",
                   name="Simulation")

#1. Getting the initial data

#Elasticity prices
elasticities = PARENT_DIR/ "data/elasticities.csv"

with open(elasticities, "r") as file:
    csv_reader = csv.DictReader(file)
    dict_elas = {}
    for row in csv_reader:
        dict_temporal = {}
        for key, value in row.items():
            if key != "Country":
                dict_temporal[key] = value
        dict_elas[row["Country"]] = dict_temporal



#Classification countries
countries = PARENT_DIR/ "data/classification_countries.csv"

with open(countries, "r") as file:
    csv_reader = csv.DictReader(file)
    dict_countries = {}
    for row in csv_reader:
        dict_temporal = {}
        for key, value in row.items():
            if key != "Economy":
                if key == "Income group":
                    if (row["Income group"] == "Lower middle income" or
                        row["Income group"] == "Upper middle income"):
                        dict_temporal[key] = "Middle income"
                    else:
                        dict_temporal[key] = value
                else:
                    dict_temporal[key] = value

        
        dict_countries[row["Economy"].upper()] = dict_temporal




#Classification NAICS
Class_NAICS = PARENT_DIR/ "data/code_NAICS_elasticity.csv"

with open(Class_NAICS, "r") as file:
    csv_reader = csv.DictReader(file)
    dict_NAICS = {}
    for row in csv_reader:
        dict_temporal = {}
        for key, value in row.items():
            if key != "NAICS":
                dict_temporal[key] = value
        dict_NAICS[row["NAICS"]] = dict_temporal

# 📌 Cargar datos desde el archivo JSON

def get_data_trade(country, exports:bool):

    if exports==True:
        value="ALL_VAL_MO"
    elif exports==False:
        value="GEN_VAL_MO"
    
    data = json.loads((get_trade_data.get_data_census("2024", None, exports, 
                        country, None)))
    
    df = pd.DataFrame(data["body"][1:], columns = data["body"][0])
    #print(df)
    df[value] = df[value].astype(float)

    df_anual = df.groupby(["NAICS_LDESC", "CTY_NAME", "NAICS"], as_index=False)[value].sum()
    df_filtrado = df_anual[df_anual["NAICS"].astype(str).str.len() == 2]
    dict_records = df_filtrado.to_dict("records")

    dict_final={}
    for element in dict_records:
        dict_temporal={}
        dict_temporal["NAICS_LDESC"]=element["NAICS_LDESC"]
        dict_temporal[value]=element[value]
        dict_final[element["NAICS"]]=dict_temporal

    return dict_final

def  get_trade_of_country(country: str):
    dict_exports=get_data_trade(country, True)
    dict_imports=get_data_trade(country, False)

    lst_NAICS=set()
    for key in dict_exports.keys():
        lst_NAICS.add(key)
        for key in dict_imports.keys():
            lst_NAICS.add(key)

    dict_final={}
    for NAIC in lst_NAICS:
        #print(NAIC)
        if not NAIC.startswith("9"):
            dict_temporal={}
            if NAIC in dict_imports:
                #print(dict_imports)
                dict_temporal["imports"]=dict_imports[NAIC]["GEN_VAL_MO"]
                dict_temporal["desciption"]=dict_imports[NAIC]["NAICS_LDESC"]
            else:
                #print("We came from here")
                dict_temporal["imports"]=0

            if NAIC in dict_exports:
                
                dict_temporal["exports"]=dict_exports[NAIC]["ALL_VAL_MO"]
                dict_temporal["desciption"]=dict_exports[NAIC]["NAICS_LDESC"]
            else:
                dict_temporal["exports"]=0

            dict_final[NAIC]=dict_temporal
        else:
            pass



    return dict_final


trade_dict={}
for country in COUNTRIES:
    trade_country=get_trade_of_country(country)
    trade_dict[country]=trade_country



# Definir opciones para los dropdowns
COUNTRIES = list(trade_dict.keys())
NAICS_CATEGORIES = [
    {"label": "11 - Agriculture and Livestock products", "value": "11"},
    {"label": "21 - Oil, Gas, Minerals and Ores", "value": "21"},
    {"label": "31 - Food, Beverage, and Tobacco Manufacturing", "value": "31"},
    {"label": "32 - Non-Heavy Manufacturing: Textile, Paper, Chemical, Pharmaceutical, etc.", "value": "32"},
    {"label": "33 - Machinery, Metal, and Equipment Manufacturing", "value": "33"}
]

tarif_values = {"5%": 0.05, "10%": 0.1, "15%": 0.15, "20%": 0.2, "25%": 0.25, "30%": 0.3,
                "50%": 0.5, "75%": 0.75, "100%": 1}



# 2. App Layout
layout = html.Div([
    html.H4("US Trade Export and Import"),
    html.P("This is a simulation to broadly estimate the impacts of a trade war between the US and other countries if mirror tariffs are adopted for both countries. "
"We measure the impact on three items: 1) The reduction in consumption of the good due to an increase in prices caused by the tariff, 2) The taxes collected by the US government, which are paid by "
"consumers when purchasing the good, and 3) The reduction in US exports as a result of decreased demand in the other country. To achieve this, we use own-price Slutsky elasticities for groups of products, "
"differentiating the elasticities by the income level of the countries involved. For this simulation, we assume the tariff is fully passed on to prices and that there is no immediate "
"substitution effect between products, which is reasonable if we consider the tariff as a shock. Additionally, we do not consider cross-price elasticities."),

    html.P("NAICS: North American Industry Classification System"),
    html.P("You can select any Country, Tariff and NAIC code for group of products"),

    html.Div([
        html.Div([
            html.Label("Select a Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in COUNTRIES],
                value="CANADA",
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select a Tariff:"),
            dcc.Dropdown(
                id='tariff-dropdown',
                options=[{'label': tariff, 'value': tariff} for tariff in tarif_values.keys()],
                value="20%",
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select a NAICS Category:"),
            dcc.Dropdown(
                id='naics-dropdown',
                options=NAICS_CATEGORIES,
                value="11",
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),

    html.Div([
        dcc.Graph(id='summary-graph', style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='import-graph', style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='export-graph', style={'width': '30%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-top': '20px'})
])


# 3. 📌 Callback principal para actualizar gráficos dinámicamente
@callback(
    [Output('summary-graph', 'figure'), Output('import-graph', 'figure'), Output('export-graph', 'figure')],
    [Input('country-dropdown', 'value'), Input('tariff-dropdown', 'value'), Input('naics-dropdown', 'value')]
)
def update_graphs(selected_country, selected_tariff, selected_naics):
    """
    Actualiza los gráficos de importaciones y exportaciones en función de las selecciones del usuario.
    """
    country_data = trade_dict.get(selected_country, {})
    naics_data = country_data.get(selected_naics, {"imports": 0, "exports": 0})

    income_group = dict_countries[selected_country]["Income group"]
    elasticity_type = dict_NAICS[selected_naics]["CLASS_ELAS"]

    elasticity_imp = float(dict_elas["High income"].get(elasticity_type, 0))
    elasticity_exp = float(dict_elas[income_group].get(elasticity_type, 0))

    tariff_value = tarif_values.get(selected_tariff, 0)
    naics_label = next((item["label"] for item in NAICS_CATEGORIES if item["value"] == selected_naics), selected_naics)

    return create_import_export_figs(
        naics_data["imports"], naics_data["exports"],
        tariff_value, elasticity_imp, elasticity_exp,
        f"Imports for {naics_label} in {selected_country}",
        f"Exports for {naics_label} in {selected_country}"
    )


# 📌 Función para generar gráficos con elasticidades
def create_import_export_figs(imports, exports, tariff, elasticity_imp, elasticity_exp, title_import, title_export):
    """
    Genera gráficos de importaciones y exportaciones considerando el efecto de un arancel con elasticidades.
    """
    adjusted_imports = imports * (1 + elasticity_imp * tariff)
    taxes = tariff * adjusted_imports
    adjusted_exports = exports * (1 + elasticity_exp * tariff)

    df_summary = pd.DataFrame({
        "Category": ["Reduction in Consumption", "Tariff payed/collected", "Reduction in Exports"],
        "USD": [imports - adjusted_imports, taxes, exports - adjusted_exports]
    })
    
    df_imports = pd.DataFrame({
        "Category": ["After Tariff", "After Tariff", "Imported in 2024"],
        "USD": [adjusted_imports, taxes, imports],
        "Type": ["Imports after tariff", "Tariff", "Imports 2024"]
    })

    df_exports = pd.DataFrame({
        "Category": ["After Tariff", "Exported in 2024"],
        "USD": [adjusted_exports, exports]
    })

    fig_summary = px.bar(df_summary, x="Category", y="USD", orientation="v",
                         title="Summary of Estimated Impact (USD)", labels={"USD": "Value (USD)"})
    fig_summary.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    fig_imports = px.bar(df_imports, x="USD", y="Category", color="Type", orientation="h",
                         title="Import Impact (USD)", barmode="stack", labels={"USD": "Value (USD)"})
    fig_imports.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    fig_exports = px.bar(df_exports, x="USD", y="Category", orientation="h",
                         title="Export Impact (USD)", barmode="stack", labels={"USD": "Value (USD)"})


    fig_exports.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return fig_summary, fig_imports, fig_exports