import plotly.express as px
from dash import Dash, dcc, html
# from dash.dependencies import Input, Output
# import numpy as np

from . import ids

df = px.data.gapminder().query("year==2007")
df["trade_amount"] = df["lifeExp"]


def render(app: Dash) -> html.Div:
    fig = px.choropleth(df, locations="iso_alpha",
                        color="trade_amount",
                        # column to add to hover information
                        hover_name="country",
                        color_continuous_scale=px.colors.sequential.Plasma)
    return html.Div(dcc.Graph(figure=fig), id=ids.MAP)
