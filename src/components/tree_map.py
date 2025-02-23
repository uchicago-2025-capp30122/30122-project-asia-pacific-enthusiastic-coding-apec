import plotly.express as px
from dash import Dash, dcc, html
#from dash.dependencies import Input, Output
import numpy as np

from . import ids

df = px.data.gapminder().query("year == 2007")


def render(app: Dash) -> html.Div:
    fig = px.treemap(df, path=[px.Constant("world"), 'continent', 'country'],
                     values='pop', color='lifeExp', hover_data=['iso_alpha'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(
                        df['lifeExp'], weights=df['pop']))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return html.Div(dcc.Graph(figure=fig), id=ids.TREE_MAP)

    # fig.show()
