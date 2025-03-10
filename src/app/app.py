import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.UNITED])

custom_order = ["Home", "Descriptive", "Treemap", "Dependance", "Simulation"]

sorted_pages = sorted(
    dash.page_registry.values(),
    key=lambda page: custom_order.index(
        page["name"]) if page["name"] in custom_order else len(custom_order)
)

app.layout = html.Div(
    children=[
        # Header Section
        dbc.Row([
            dbc.Col(
                html.H1("Trade and Production Insights",
                        className="text-white"),
                width={"size": 8, "offset": 2},
                ),
            dbc.Col(
                html.H3("Exploring U.S. Trade and Production Dynamics",
                        className="text-white"),
                width={"size": 8, "offset": 2},
            ),
            ],
            style={"background-color": "#003366", "padding": "30px 0"},
        ),

        # Navigation and Content Section
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Div(
                        dcc.Link(f"{page['name']}",
                                 href=page["relative_path"],
                                 className="btn btn-link text-dark mb-2")
                                 ) for page in sorted_pages
                    ],
                    className="d-flex flex-wrap justify-content-start",
                    ),
                width=3,
                style={
                    "display": "block",
                    "background-color": "#F4F6F9",
                    "padding": "10px",  # Increase padding for a cleaner look
                    "border-radius": "8px",  # Softer corners
                    "border": "2px solid #ddd",
                    },
                ),
            dbc.Col(
                dash.page_container,
                width=10,
                style={
                    "margin-left": "15px",
                    "margin-top": "7px",
                    "margin-right": "15px",
                    "background-color": "#FFFFFF",
                },
            ),
            ]
        ),

        # Footer Section
        dbc.Row([
            dbc.Col(
                html.P(
                    "This project was done for the CAPP 30122 Winter 2025 "
                    "course by Tina Dou, José Pajuelo, Ryota Shimizu, and "
                    "Mauro Ttito.",
                    className="text-center text-muted",
                    ),
                width=12,
            ),
            ],
            style={"background-color": "#66A3D2", "padding": "20px 0"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
