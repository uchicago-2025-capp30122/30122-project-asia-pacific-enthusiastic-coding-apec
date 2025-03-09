import dash
from dash import html

# 0. Register as Dash page
dash.register_page(__name__, path="/")

# 1. App Layout

layout = html.Div(
    [
        html.H3("Welcome to Trade and Production Insights"),
        html.P(
            "We build this dashboard to analyze U.S. trade and production data"
            " to understand key trends in production and the flow of goods."
        ),
        html.P(
            "We use data combined with economic analysis to create interactive"
            " visualizations."
        ),
        html.P(
            "This project aims to provide insights into "
            "traded products, their origins and destinations, as well as the "
            "concentration of production across industries."
        ),
        html.H4("Data Sources"),
        html.P("We rely on the following data sets:"),
        html.Div(
            id="data_sources_list",
            children=[
                html.Ul(
                    id="actual_list",
                    children=[
                        html.Li(
                            "Trade Data: Extracted using Python scripts that "
                            "clean and process trade data, providing insights "
                            "into the flow of goods."
                        ),
                        html.Li(
                            "Production Data: Integrated production data "
                            "includes information about various industries "
                            "and agricultural outputs."
                        ),
                        html.Li(
                            "Market Concentration: We calculate the "
                            "Herfindahl-Hirschman Index (HHI) to analyze "
                            "market concentration across cities in the U.S."
                        ),
                    ],
                )
            ],
        ),
        html.H4("Libraries"),
        html.P(
            "We use Python 3.13.1 for data processing, with libraries like "
            "Pandas for cleaning and analysis. The data is visualized through "
            "a Dash app using Plotly."
        ),
    ]
)

"""
        html.Iframe(
                    src="https://www.youtube.com/embed/IT7vDqm4xiY?autoplay=1",
                    width="100%",
                    height="500px",  # Adjust the height as needed
                    style={
                        "border": "none",
                        "border-radius": "5px",
                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
                    },
                    ),
"""
