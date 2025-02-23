from dash import Dash, html
from . import nation_dropdown, bar_chart, tree_map, map, hh_index_bubble


def create_layout(app: Dash) -> html.Div:
    return html.Div(
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
            hh_index_bubble.render(app),
            bar_chart.render(app),
        ],
    )
