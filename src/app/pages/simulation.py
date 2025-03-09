import dash
from dash import html

# 0. Register as Dash page
dash.register_page(__name__, path="/simulation",
                   title="Simulation",
                   name="Simulation")

# 1. App Layout

layout = html.Div()