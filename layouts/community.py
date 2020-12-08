from typing import Dict, List

import assets.texts as texts
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import numpy as np
import wojciech as w
from app import app
from dash.dependencies import Input, Output
from project.library_functions import (
    draw_overlaps_plotly,
)
from project.library_functions.config import Config

from utils.community_graphs import build_cytoscape_elements, make_stylesheet

from utils.data import (
    graph_reddit_gcc,
    graph_wiki,
    layout_reddit,
    layout_wiki,
)


####################################
############ Generate elements #####
####################################
print("Building cytoscape graphs")
elements_wiki, properties_wiki = build_cytoscape_elements(
    graph_wiki,
    positions=layout_wiki,
    node_attributes=[
        "mechanism_category",
        "effect_category",
        "louvain_community_wiki_L0",
        "louvain_community_wiki_L1",
    ],
)
elements_reddit, properties_reddit = build_cytoscape_elements(
    graph_reddit_gcc,
    positions=layout_reddit,
    node_attributes=[
        "mechanism_category",
        "effect_category",
        "louvain_community_reddit_R1.00_L0",
        "louvain_community_reddit_R0.60_L0",
        "louvain_community_wiki_L0",
        "louvain_community_wiki_L1",
    ],
)

stylesheet_wiki, legend_wiki = make_stylesheet(properties_wiki)
stylesheet_reddit, legend_reddit = make_stylesheet(properties_reddit)

cyto_graph_wiki = cyto.Cytoscape(
    id="cyto_graph_wiki",
    layout={"name": "preset"},
    responsive=True,
    zoom=0.1,
    minZoom=0.05,
    maxZoom=3,
    style={"width": "100%", "height": "500px"},
    stylesheet=stylesheet_wiki,
    elements=elements_wiki,
)

cyto_graph_reddit = cyto.Cytoscape(
    id="cyto_graph_reddit",
    layout={"name": "preset"},
    responsive=True,
    zoom=0.3,
    minZoom=0.1,
    maxZoom=3,
    style={"width": "100%", "height": "500pt"},
    stylesheet=stylesheet_reddit,
    elements=elements_reddit,
)

print("Computing 2D-heatmaps of category overlaps")
hist2d_louvain_1_vs_effects = draw_overlaps_plotly(
    "louvain_community_wiki_L0",
    "effect_category",
    graph_wiki,
    saved="hist2d_louvain_1_vs_effects",
)
hist2d_louvain_1_vs_mechanisms = draw_overlaps_plotly(
    "louvain_community_wiki_L0",
    "mechanism_category",
    graph_wiki,
    saved="hist2d_louvain_1_vs_mechanisms",
)

hist2d_louvain_2_vs_effects = draw_overlaps_plotly(
    "louvain_community_wiki_L1",
    "effect_category",
    graph_wiki,
    saved="hist2d_louvain_2_vs_effects",
)
hist2d_louvain_2_vs_mechanisms = draw_overlaps_plotly(
    "louvain_community_wiki_L1",
    "mechanism_category",
    graph_wiki,
    saved="hist2d_louvain_2_vs_mechanisms",
)

hist2d_louvain_reddit_vs_effects = draw_overlaps_plotly(
    "louvain_community_reddit_L0",
    "effect_category",
    graph_reddit_gcc,
    saved="hist2d_louvain_reddit_vs_effects",
)
hist2d_louvain_reddit_vs_mechanisms = draw_overlaps_plotly(
    "louvain_community_reddit_L0",
    "mechanism_category",
    graph_reddit_gcc,
    saved="hist2d_louvain_reddit_vs_mechanisms",
)
####################################
############ Layout elements #####
####################################
community_layout = html.Div(
    [
        dcc.Store(id="wiki_legend_store"),
        dcc.Store(id="reddit_legend_store"),
        html.H3(
            children=[
                "Finding",
                html.Em(" Communities "),
                ": which substances are often mentionned together?".title(),
            ]
        ),
        html.P(
            "Now that we have looked at how the graphs are built, we can get to the meat of it: actually analyzing usage patterns."
        ),
        html.P(
            "Our idea is that by looking at which nootropics are most often mentionned together,\
            it may possible to derive information about what the most popular combinations of \
                nootropics are, and how they relate to one another."
        ),
        html.H4("Wikipedia Communities"),
        html.P(
            "To get a feel for how this works, let's start by looking at the communities that are detected on WikiPedia.\
            The dataset is simpler (much fewer links), and we found that the separation into communities was much clearer."
        ),
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col(cyto_graph_wiki, width=9),
                        dbc.Col(
                            children=[
                                dbc.FormGroup(
                                    [
                                        dbc.Label(
                                            "Color nodes by:",
                                        ),
                                        dbc.Select(
                                            id="select_root_category_wiki",
                                            options=[
                                                {
                                                    "label": "None",
                                                    "value": "none",
                                                },
                                                {
                                                    "label": "Wikipedia Categories",
                                                    "value": "wikicats",
                                                    "disabled": True,
                                                },
                                                {
                                                    "label": "Mechanism of Action",
                                                    "value": "mechanism",
                                                },
                                                {
                                                    "label": "Psychological Effect",
                                                    "value": "effect",
                                                },
                                                {
                                                    "label": "Autodetected Communities",
                                                    "value": "auto",
                                                    "disabled": True,
                                                },
                                                {
                                                    "label": "Louvain Categories - Top Level",
                                                    "value": "louvain_1",
                                                },
                                            ],
                                            value="none",
                                        ),
                                    ]
                                ),
                                dbc.Row(id="wiki_plot_legend", children=[]),
                            ],
                            width=3,
                        ),
                    ]
                ),
                dbc.Row(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("More Info", className="card-title"),
                                html.Div(
                                    "The network above was layed out using the ForceAtlas algorithm, which uses a physical simulation\
                                    to spread out nodes in a way that edges act as 'elastics' and nodes as repulsors. This has the effect of \
                                    drawing densely-connected regions of the graph as clusters (many edges that attract the nodes to each other), \
                                    and to push isolated nodes or unrelated communities far from one another.\
                                    To learn more about how this clustering reflects both the actual structure of the articles and the communities that can\
                                    be determined by using network analysis algorithm, select one of the coloring schemes above.",
                                    className="card-text",
                                ),
                                html.Div(
                                    "",
                                    className="card-text",
                                    id="cyto_graph_wiki_info",
                                ),
                            ]
                        ),
                    ),
                ),
            ]
        ),
        html.Hr(),
        html.H4("Reddit Communities"),
        html.P(
            "Here comes one of the main questions we had when setting out to analyse our data: can we actually derive information about the underlying properties of nootropics\
            starting from just reddit discussions? The following visualization is similar to the above, except here all links are extracted by finding nootropics that are mentionned together in reddit posts.",
            style={"margin-bottom": "12em"},
        ),
        dbc.Container(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            children=[
                                dbc.FormGroup(
                                    [
                                        dbc.Label(
                                            "Select the attribute by which to color the nodes"
                                        ),
                                        dbc.Select(
                                            id="select_root_category_reddit",
                                            options=[
                                                {
                                                    "label": "None",
                                                    "value": "none",
                                                },
                                                {
                                                    "label": "Wikipedia Categories",
                                                    "value": "none",
                                                    "disabled": True,
                                                },
                                                {
                                                    "label": "Mechanism of Action",
                                                    "value": "mechanism",
                                                },
                                                {
                                                    "label": "Psychological Effect",
                                                    "value": "effect",
                                                },
                                                {
                                                    "label": "Autodetected Communities (on reddit)",
                                                    "value": "none",
                                                    "disabled": True,
                                                },
                                                {
                                                    "label": "Louvain Categories - Coarse Grained",
                                                    "value": "louvain_reddit",
                                                },
                                                {
                                                    "label": "Louvain Categories - Fine Grained",
                                                    "value": "louvain_reddit_r07",
                                                },
                                            ],
                                            value="louvain_reddit",
                                        ),
                                    ]
                                ),
                                dbc.Row(id="reddit_plot_legend", children=[]),
                            ],
                            width=3,
                        ),
                        dbc.Col(cyto_graph_reddit, width=9),
                    ]
                ),
                dbc.Row(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("More Info", className="card-title"),
                                html.Div(
                                    children=[
                                        html.P(
                                            children=[
                                                "It's immediately clear that the clustering doesn't work as well in this case: most of the nodes form a big blob in the center.\
                                    There are several reasons to this, and the main one is that this graph is very densely connected - in network science terms, it's \
                                    closer to a ",
                                                html.Em("random network"),
                                                " than to a ",
                                                html.Em("scale-free network"),
                                                ' like the WikiPedia network above. While it is still possible to find "nicer" layouts than what you see above, the python \
                                                implementation of the force-atlas 2 algorithm is quite limited, and that is the best that we were able to do. \
                                                Once more, you are invited to chose different coloring schemes to see the effects of automatic community detection.',
                                            ]
                                        )
                                    ],
                                    className="card-text",
                                ),
                                html.Hr(),
                                html.Div(
                                    "",
                                    className="card-text",
                                    id="cyto_graph_reddit_info",
                                ),
                            ]
                        ),
                    ),
                ),
            ]
        ),
    ]
)


####################################
############ Callbacks #############
####################################
@app.callback(
    [
        Output("cyto_graph_wiki", "stylesheet"),
        Output("wiki_legend_store", "data"),
        Output("cyto_graph_wiki_info", "children"),
    ],
    Input("select_root_category_wiki", "value"),
)
def display_wiki_graph_info(value):
    print("changed category")
    if not value or value == "none":
        stylesheet, legend = make_stylesheet(properties_wiki)

    elif value == "effect":
        stylesheet, legend = make_stylesheet(
            properties_wiki, color_node_by="mechanism_category"
        )

    elif value == "mechanism":
        stylesheet, legend = make_stylesheet(
            properties_wiki, color_node_by="effect_category"
        )
    elif value == "louvain_1":
        stylesheet, legend = make_stylesheet(
            properties_wiki, color_node_by="louvain_community_wiki_L0"
        )
        # doesn't make sense to show legend since communities are arbitrary
        legend = {}
    elif value == "louvain_2":
        stylesheet, legend = make_stylesheet(
            properties_wiki, color_node_by="louvain_community_wiki_L1"
        )
        # doesn't make sense to show legend since communities are arbitrary
        legend = {}
    if not legend:
        legend = {}

    ## Compute Info texts
    if not value or value == "none":
        children = []
    elif value in ["effect", "mechanism"]:
        children = [
            html.Hr(),
            html.H4("Wikipedia Categories"),
            html.P(
                children=[
                    "The ",
                    html.A(
                        "Drugs by psychological effects",
                        href="https://en.wikipedia.org/wiki/Category:Drugs_by_psychological_effects",
                    ),
                    " and ",
                    html.A(
                        "Psychoactive drugs by mechanism of action",
                        href="https://en.wikipedia.org/wiki/Category:Psychoactive_drugs_by_mechanism_of_action",
                    ),
                    " are the two main WikiPedia categories by which the substances can be categorized. \
                    As you can see, the ForceAtlas algorithm shows that these categories are quite well represented \
                    in the way that the nodes link to each other: looking at the coloring by effect, stimulants are all on top, \
                    Psycholeptics are on the bottom-left, etc. Interestingly, there is a big cluster of nodes on the right that have no category:\
                    Those are actually supplements (vitamins etc.), which aren't categorized here.   \
                    One neat thing about these two colorings is that they can show which effects are related to which mechanisms:\
                    For instance, 'Excitatory Amino Acid Receptor Ligands' seem to all be psychoanaleptics, while \
                    'GABA receptor ligands'  are psychoanaleptics.",
                ]
            ),
        ]
    elif value == "louvain_1":

        children = [
            html.Hr(),
            html.H5("Comparing autodetected communities to wikipedia categories"),
            html.P(
                children=[
                    "The two 2-D histograms below show, for each detected community (L0-...),\
                 the overlap of that community with each of the categories on wikipedia. \
                     "
                ]
            ),
            html.H6("Drugs by mechanism of action"),
            dcc.Graph(figure=hist2d_louvain_1_vs_mechanisms),
            html.P(
                children=[
                    "There are two categories that have a sizeable overlap with the communities detected by the algorithm: ",
                    html.Em("GABA receptor ligands"),
                    " and ",
                    html.Em("Monoamine releasing agents"),
                    ". It's curious that these specific two categories were recognized by the algorithm - and it may be interesting, \
                had we more time, to investigate why.",
                ]
            ),
            html.H6("Drugs by Psychological Effect"),
            dcc.Graph(figure=hist2d_louvain_1_vs_effects),
            html.P(
                children=[
                    "In this case, there is only one community and one category which were found to have a sizeable overlap: ",
                    html.Em("Stimulants"),
                    ". Once more, we are unsure why this specific community was the only one to have a significan overlap - but it is interesting to see that there is at least ",
                    html.Em("some "),
                    "overlap between autodetected communities and existing categories of the corresponding nodes.",
                ]
            ),
        ]
    else:
        children = []

    return [stylesheet, legend, children]


@app.callback(
    Output("wiki_plot_legend", "children"),
    Input("wiki_legend_store", "data"),
)
def show_legends_wiki(data):
    print("changed category")
    if not data or data == {}:
        return []

    else:
        body = []
        for name, color in sorted(data.items(), key=lambda x: x[0]):
            body.append(
                html.Tr(
                    [
                        html.Th(
                            html.Span("⬤", style={"color": color}),
                            style={"padding": "0.5rem"},
                        ),
                        html.Td(
                            f"{name.title().replace('_', ' ')}",
                            style={"padding": "0.5rem"},
                        ),
                    ]
                ),
            )

        children = html.Div(
            dbc.Table(
                children=[
                    html.Thead("Legend"),
                    html.Tbody(body),
                ],
                borderless=True,
                striped=True,
                hover=True,
            ),
            style={"max-height": "400px", "overflow": "scroll"},
        )
        return children


@app.callback(
    [
        Output("cyto_graph_reddit", "stylesheet"),
        Output("reddit_legend_store", "data"),
        Output("cyto_graph_reddit_info", "children"),
    ],
    Input("select_root_category_reddit", "value"),
)
def display_reddit_graph_info(value):
    print("changed category")
    if not value or value == "none":
        stylesheet, legend = make_stylesheet(properties_reddit)

    elif value == "effect":
        stylesheet, legend = make_stylesheet(
            properties_reddit, color_node_by="mechanism_category"
        )

    elif value == "mechanism":
        stylesheet, legend = make_stylesheet(
            properties_reddit, color_node_by="effect_category"
        )
    elif value == "louvain_reddit":
        stylesheet, legend = make_stylesheet(
            properties_reddit, color_node_by="louvain_community_reddit_R1.00_L0"
        )
        # doesn't make sense to show legend since communities are arbitrary
        legend = {}
    elif value == "louvain_reddit_r07":
        stylesheet, legend = make_stylesheet(
            properties_reddit, color_node_by="louvain_community_reddit_R0.60_L0"
        )
        # doesn't make sense to show legend since communities are arbitrary
        legend = {}
    if not legend:
        legend = {}

    ## Compute Info texts
    if not value or value == "none":
        children = []
    elif value in ["effect", "mechanism"]:
        children = [
            html.H4("Wikipedia Categories... again"),
            html.P(
                children=[
                    "Out of curiosity, we tried to color the nodes on the extracted reddit network by using the categories that we took from wikipedia. The \
                    idea was that if the network structure reflected those categories, they would appear as spatially well-defined areas in the network.\
                    As you can see, the results were mixed: when coloring by",
                    html.Em("mechanism of action"),
                    "there is one large area that is covered by",
                    html.Em("psychoanaleptics"),
                    ", but little else is visible (in fact, the rest of the network has mostly no category under this categorization).\
                    ",
                ]
            ),
        ]
    elif value == "louvain_reddit":

        children = [
            html.H4("Autodetected Categories"),
            html.P(
                "Once more, we used the louvain algorithm to autodetect communities in the graph. \
                And, once more, we looked at how those communities overlap with the two main categorizations we chose."
            ),
            dcc.Graph(figure=hist2d_louvain_reddit_vs_effects),
            dcc.Graph(figure=hist2d_louvain_reddit_vs_mechanisms),
        ]
    else:
        children = []

    return [stylesheet, legend, children]


@app.callback(
    Output("reddit_plot_legend", "children"),
    Input("reddit_legend_store", "data"),
)
def show_legends_reddit(data):
    print("changed category")
    if not data or data == {}:
        return []

    else:
        body = []
        for name, color in sorted(data.items(), key=lambda x: x[0]):
            body.append(
                html.Tr(
                    [
                        html.Th(
                            html.Span("⬤", style={"color": color}),
                            style={"padding": "0.5rem"},
                        ),
                        html.Td(
                            f"{name.title().replace('_', ' ')}",
                            style={"padding": "0.5rem"},
                        ),
                    ]
                ),
            )

        children = html.Div(
            dbc.Table(
                children=[
                    html.Thead("Legend"),
                    html.Tbody(body),
                ],
                borderless=True,
                striped=True,
                hover=True,
            ),
            style={"max-height": "400px", "overflow": "scroll"},
        )
        return children
