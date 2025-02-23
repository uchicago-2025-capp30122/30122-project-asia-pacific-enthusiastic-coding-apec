import plotly.express as px
from dash import Dash, dcc, html
#from dash.dependencies import Input, Output
import numpy as np

from . import ids

df = px.data.gapminder().query("year==2007")
df.head()


def render(app: Dash) -> html.Div:
    fig = px.choropleth(df, locations="iso_alpha",
                        color="lifeExp", # lifeExp is a column of gapminder
                        hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    return html.Div(dcc.Graph(figure=fig), id=ids.MAP)
