from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import datetime

def render() -> html.Div:
    current_year = datetime.datetime.now().year
    month_list = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    return html.Div(
        children=[
            html.H6("Year and Month"),
            html.Label("Year:"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": str(year)} 
                         for year in range(2010, current_year)],
                value=str(current_year - 1), 
                multi=False,
            ),
            html.Label("Month:"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} 
                         for month in month_list],
                value="01",
                multi=False
            ),
            dcc.Graph(id=ids.HHINDEX_CHART)])