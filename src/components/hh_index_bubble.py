import plotly.express as px
from dash import Dash, dcc, html
# from dash.dependencies import Input, Output
# import numpy as np

from . import ids

df = px.data.gapminder()
df["trade_amount"] = df["lifeExp"]


def render(app: Dash) -> html.Div:
    fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="trade_amount",
                     size="pop", color="continent",
                     hover_name="country", log_x=True, size_max=60)
    return html.Div(dcc.Graph(figure=fig), id=ids.HHINDEX_CHART)
