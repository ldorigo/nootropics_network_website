# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import dash

import wojciech as w
from project.library_functions.config import Config
from project.library_functions import plotly_draw
from dash_bootstrap_components.themes import *

available_themes = [
    CERULEAN,
    COSMO,
    CYBORG,
    DARKLY,
    FLATLY,
    JOURNAL,
    LITERA,
    LUMEN,
    LUX,
    MATERIA,
    MINTY,
    PULSE,
    SANDSTONE,
    SIMPLEX,
    SKETCHY,
    SLATE,
    SOLAR,
    SPACELAB,
    SUPERHERO,
    UNITED,
    YETI,
]

# TODO: Replace with a dedicated stylesheet
# external_stylesheets = [
#     "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css"
# ]

external_stylesheets = [MATERIA]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
# Required for gunicorn
server = app.server
