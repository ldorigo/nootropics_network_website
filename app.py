# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

# TODO: Replace with a dedicated stylesheet
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Required for gunicorn
server = app.server




app.layout = html.Div(
    children=[
        html.H1(children="Social Graphs and Interactions: Analyzing Nootropics Networks"),
        html.Div(
            children=
                """
                TODO: Introduction text
                """
        ),
    ]
)


# @app.callback(
#     Output(component_id="graph", component_property="figure"),
#     [
#         Input(component_id="halflife_input", component_property="value"),
#         Input(component_id="absorption_constant_input", component_property="value"),
#     ],
#     [
#         State(component_id="blood_volume_input", component_property="value")
#     ],
# )
# def update_halflife_in_figure(ka: float, blood_volume:float, halflife: float):
#     if halflife:
#         ke = firstorder.te_1_2_to_ke(halflife)
#         sol = firstorder.firstorder_absorption_firstorder_elimination(
#             ke=ke, 
#             ka=ka,
#             bioavailability=0.99,
#             duration=24, blood_volume= blood_volume,doses=[100],timings=[0]
#         )
#         fig = px.line(x=sol["t"], y=sol["y"])
#         return fig


if __name__ == "__main__":
    app.run_server(debug=True)