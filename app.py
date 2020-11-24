# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from bokeh import embed, plotting
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import wojciech as w
from project.config import Config
from fa2 import ForceAtlas2
from project.library_functions import  plotly_draw
import networkx as nx


# TODO: Replace with a dedicated stylesheet
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Required for gunicorn
server = app.server



graph_reddit : nx.Graph
graph_wiki : nx.Graph
graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_gcc)
graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)


forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=True,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=0.5,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=1,
                        strongGravityMode=True,
                        gravity=0.001,

                        # Log
                        verbose=True)

positions_wiki = forceatlas2.forceatlas2_networkx_layout(graph_wiki, pos=None, iterations=1000)
# positions_reddit = forceatlas2.forceatlas2_networkx_layout(graph_reddit, pos=None, iterations=1000)
# %%


test_figure = plotly_draw.draw_graph_plotly(
    graph = graph_wiki,
    positions=positions_wiki
)

app.layout = html.Div(
    children=[
        html.H1(children="Social Graphs and Interactions: Analyzing Nootropics Networks"),
        dcc.Graph(figure = test_figure)
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