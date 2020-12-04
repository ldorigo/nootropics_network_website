from project.library_functions.communities import assign_louvain_communities
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
    assign_root_categories,
    create_graph_reddit,
    create_graph_wiki,
    draw_graph_plotly,
    get_fa2_layout,
    get_name_by,
    get_root_category_mapping,
    get_top,
    get_top_posts,
    get_wiki_data,
    draw_overlaps_plotly,
)
from project.library_functions.config import Config
from project.library_functions.create_graph_wiki import create_graph_wiki
from project.library_functions.layouting import get_fa2_layout

from utils.community_graphs import build_cytoscape_elements, make_stylesheet

## initialization

print("Displaying community page. Loading graphs...")
graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_gcc)
graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)
print("Loading/computing layouts...")
graph_reddit = w.graph.largest_connected_component(
    create_graph_reddit(
        max_drugs_in_post=8,
        min_content_length_in_characters=30,
        min_edge_occurrences_to_link=2,
    )
)
graph_wiki = w.graph.largest_connected_component(create_graph_wiki().to_undirected())
layout_reddit = get_fa2_layout(
    graph_reddit,
    edge_weight_attribute="count",
    saved="reddit_filtered_weighted_gcc.json",
)
layout_wiki = get_fa2_layout(graph_wiki, saved="wiki_simple_noargs_gcc.json")
## Assign "root categories" on wikipedia
print("Assigning root categories...")
assign_root_categories(
    graph_wiki,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="effects"),
    name="effect_category",
)

assign_root_categories(
    graph_wiki,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="mechanisms"),
    name="mechanism_category",
)
assign_root_categories(
    graph_reddit,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="effects"),
    name="effect_category",
)
assign_root_categories(
    graph_reddit,
    wiki_data=get_wiki_data(),
    mapping=get_root_category_mapping(which="mechanisms"),
    name="mechanism_category",
)

## Assign louvain communities on both networks
print("Assigning Louvain categories")
_, reddit_dendrogram, _, wiki_dendrogram = assign_louvain_communities(
    graph_reddit, graph_wiki, reddit_edge_weight="count", others_threshold=4
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
    graph_reddit,
    positions=layout_reddit,
    node_attributes=[
        "mechanism_category",
        "effect_category",
        "louvain_community_reddit_L0",
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
    minZoom=0.5,
    maxZoom=3,
    style={"width": "600pt", "height": "800pt"},
    stylesheet=stylesheet_wiki,
    elements=elements_wiki,
)

cyto_graph_reddit = cyto.Cytoscape(
    id="cyto_graph_reddit",
    layout={"name": "preset"},
    responsive=True,
    minZoom=0.5,
    maxZoom=3,
    style={"width": "600pt", "height": "800pt"},
    stylesheet=stylesheet_reddit,
    elements=elements_reddit,
)

print("Computing 2D-heatmaps of category overlaps")
plot_louvain_1_vs_effects = draw_overlaps_plotly(
    "louvain_community_wiki_L0", "effect_category", graph_wiki
)
plot_louvain_1_vs_mechanisms = draw_overlaps_plotly(
    "louvain_community_wiki_L0", "mechanism_category", graph_wiki
)

plot_louvain_2_vs_effects = draw_overlaps_plotly(
    "louvain_community_wiki_L1", "effect_category", graph_wiki
)
plot_louvain_2_vs_mechanisms = draw_overlaps_plotly(
    "louvain_community_wiki_L1", "mechanism_category", graph_wiki
)
####################################
############ Layout elements #####
####################################
community_layout = html.Div(
    [
        dcc.Store(id="wiki_legend_store"),
        dcc.Store(id="reddit_legend_store"),
        html.H3(
            "Finding 'communities': which substances are often mentionned together?"
        ),
        html.P(
            "Now that we have looked at how the graphs are built, we can get to the meat of it: actually analyzing usage patterns."
        ),
        html.P(
            "Our idea is that by looking at which nootropics are most often mentionned together, it's possible to derive information about\
        what the most common combinations of nootropics are, and how they relate to one another."
        ),
        html.H4("Wikipedia Communities"),
        html.P(
            "To get a feel for how this works, let's start by looking at the communities that are detected on WikiPedia. The dataset is simpler (much fewer links), and we found that the separation into communities was much clearer."
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
                                            id="select_root_category_wiki",
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
                                                    "label": "Autodetected Communities",
                                                    "value": "none",
                                                    "disabled": True,
                                                },
                                                {
                                                    "label": "Louvain Categories - Top Level",
                                                    "value": "louvain_1",
                                                },
                                                {
                                                    "label": "Louvain Categories - Level 2",
                                                    "value": "louvain_2",
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
                        dbc.Col(cyto_graph_wiki, width=9),
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
                                html.Hr(),
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
        html.H4("Reddit Communities"),
        html.P(
            "Here comes one of the main questions we had when setting out to analyse our data: can we actually derive information about the underlying properties of nootropics\
            starting from just reddit discussions? The following visualization is similar to the above, except here all links are extracted by finding nootropics that are mentionned together in reddit posts."
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
                                                    "label": "Louvain Categories - Top Level",
                                                    "value": "louvain_reddit",
                                                },
                                            ],
                                            value="none",
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
                                    "",
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
            dcc.Graph(figure=plot_louvain_1_vs_mechanisms),
            dcc.Graph(figure=plot_louvain_1_vs_effects),
        ]
    elif value == "louvain_2":

        children = [
            dcc.Graph(figure=plot_louvain_2_vs_mechanisms),
            dcc.Graph(figure=plot_louvain_2_vs_effects),
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
        children = []
        for name, color in sorted(data.items(), key=lambda x: x[0]):
            children.append(
                html.P(
                    children=[
                        html.Span("⬤", style={"color": color}),
                        f" - {name.title().replace('_', ' ')}",
                    ]
                )
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
            properties_reddit, color_node_by="louvain_community_reddit_L0"
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
            html.H4("redditpedia Categories"),
            html.P(
                children=[
                    "The ",
                    html.A(
                        "Drugs by psychological effects",
                        href="https://en.redditpedia.org/reddit/Category:Drugs_by_psychological_effects",
                    ),
                    " and ",
                    html.A(
                        "Psychoactive drugs by mechanism of action",
                        href="https://en.redditpedia.org/reddit/Category:Psychoactive_drugs_by_mechanism_of_action",
                    ),
                    " are the two main redditPedia categories by which the substances can be categorized. \
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
            dcc.Graph(figure=plot_louvain_1_vs_mechanisms),
            dcc.Graph(figure=plot_louvain_1_vs_effects),
        ]
    elif value == "louvain_2":

        children = [
            dcc.Graph(figure=plot_louvain_2_vs_mechanisms),
            dcc.Graph(figure=plot_louvain_2_vs_effects),
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
        children = []
        for name, color in sorted(data.items(), key=lambda x: x[0]):
            children.append(
                html.P(
                    children=[
                        html.Span("⬤", style={"color": color}),
                        f" - {name.title().replace('_', ' ')}",
                    ]
                )
            )
        return children
