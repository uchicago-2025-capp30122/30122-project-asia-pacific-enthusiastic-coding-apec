from dash import Dash, html
from . import nation_dropdown, bar_chart, tree_map, map, time_dropdown, hh_index_bubble, dependency, naics_dropdown


def create_layout(app: Dash) -> html.Div:
    return html.Div([
        html.Div(
            className="app-div",
            children=[
                html.H1(app.title),
                html.Hr(),
                html.Div(
                    className="dropdown-container",
                    children=[
                        nation_dropdown.render(app)
                    ]
                ),
                map.render(app),
                tree_map.render(app),
                bar_chart.render(app),
            ]),
        html.Div(
            className="hhi-div",
            children=[
                html.H1(app.title),
                html.Hr(),
                html.Div(
                    className="dropdown-container",
                    children=[time_dropdown.render()]
                ),
                hh_index_bubble.render(app)
            ]),
        html.Div(
            className="independency-div",
            children=[
                html.H1(app.title),
                html.Hr(),
                html.Div(
                    className="dropdown-container",
                    children=[naics_dropdown.render()]
                ),
                dependency.render(app)
            ]),
    ])
        
