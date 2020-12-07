import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from layouts import homepage, preliminary, community, text_analysis
import callbacks
from typing import Dict

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Home", href="/page-1", id="page-1-link"),
                dbc.NavLink("Preliminary Analysis", href="/page-2", id="page-2-link"),
                dbc.NavLink("Happy and sad networks", href="/page-3", id="page-3-link"),
                dbc.NavLink("Communities", href="/page-4", id="page-4-link"),
                dbc.NavLink("Text Analysis", href="/page-5", id="page-5-link"),
            ],
            brand="Nootropics & Graphs",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return homepage.homepage_layout
    elif pathname == "/page-2":
        return preliminary.preliminary_layout
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    elif pathname == "/page-4":
        return community.community_layout
    elif pathname == "/page-5":
        return text_analysis.text_analysis_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
