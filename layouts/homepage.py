import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Hr import Hr
import assets.texts as texts
import dash_bootstrap_components as dbc


reddit_table = dbc.Table(
    children=[
        html.Thead("Reddit Data"),
        html.Tbody(
            [
                html.Tr([html.Th("Number of Posts"), html.Td("108.588")]),
                html.Tr(
                    [
                        html.Th("Total Size of the Dataset"),
                        html.Td("~65 MB (after cleaning)"),
                    ]
                ),
                html.Tr(
                    [
                        html.Th("Recorded Variables"),
                        html.Td("Title, Author, Contents, Date"),
                    ]
                ),
                html.Tr([html.Th("Average post length"), html.Td("426 Characters")]),
                html.Tr(
                    [html.Th("Average Nootropics mentions per post"), html.Td("1")]
                ),
                html.Tr(
                    [html.Th("Number of posts with 2+ nootropics"), html.Td("23.361")]
                ),
            ]
        ),
    ],
    borderless=True,
    striped=True,
    hover=True,
)

wiki_table = dbc.Table(
    children=[
        html.Thead("Wikipedia Data"),
        html.Tbody(
            [
                html.Tr([html.Th("Number of Pages"), html.Td("1.502")]),
                html.Tr([html.Th("Total Size of the Dataset"), html.Td("~10MB")]),
                html.Tr(
                    [
                        html.Th("Recorded Variables"),
                        html.Td(
                            "Name (title), Categories', Content', Links, Redirects (synonyms), URL"
                        ),
                    ]
                ),
                html.Tr([html.Th("Average page length"), html.Td("4.798 Characters")]),
                html.Tr(
                    [
                        html.Th("Average number of links towards another nootropic"),
                        html.Td("2.77"),
                    ]
                ),
            ]
        ),
    ],
    borderless=True,
    striped=True,
    hover=True,
)

homepage_explainer_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Explainer Notebook", className="card-title"),
            html.P(
                "This is the notebook containing our more lengthy and technical analysis. Non-interactive, only for viewing."
            ),
            dbc.CardLink(children="Open on nbviewer", href="TODO"),
        ]
    )
)
homepage_repo_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("GitHub Repository", className="card-title"),
            html.P(
                "GitHub repository containing all our data and code. For playing around/executing on your own computer."
            ),
            dbc.CardLink(children="Open on GitHub", href="TODO"),
        ]
    )
)
link_cards = dbc.CardDeck(children=[homepage_explainer_card, homepage_repo_card])
homepage_layout = html.Div(
    [
        html.H2(texts.welcome_title),
        html.P(texts.welcome_text),
        html.Hr(),
        html.H2("Our Data"),
        dbc.Container(dbc.Row([dbc.Col(reddit_table), dbc.Col(wiki_table)])),
        html.Hr(),
        html.H2("Links and References"),
        link_cards,
    ]
)
