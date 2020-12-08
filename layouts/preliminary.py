import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from utils.utils import make_table_from_items
from dash.dependencies import Input, Output
from project.library_functions import (
    get_name_by,
    get_top,
    get_top_posts,
    get_wiki_plots_figure,
    get_reddit_plots_figure,
)
from app import app
from utils.data import (
    all_names_and_synonyms,
    synonym_mapping,
    graph_reddit,
    graph_wiki_directed,
)
from utils.preliminary import wiki_page, reddit_substance

wiki_preliminary_plots = get_wiki_plots_figure()
reddit_preliminary_plots = get_reddit_plots_figure()


preliminary_layout = html.Div(
    [
        html.H2("Preliminary Analysis"),
        html.P(
            "Let's get a quick overview of our data, from both wikipedia and Reddit."
        ),
        html.Hr(className="my-3"),
        html.H3("Wikipedia Pages"),
        html.P(
            "All our further analysis is based on the data we extracted from WikiPedia, so it's worth taking a deeper look at it."
        ),
        html.P(
            "The data we took from WikiPedia consists of around 1.500 articles, \
            corresponding roughly to pages under two main categories: dietary \
                supplements, and psychoactive drugs. Let's look at the \
                    distributions of some of the page's attributes."
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Some Histograms", className="card-title"),
                    dcc.Graph(
                        figure=wiki_preliminary_plots, id="wiki_preliminary_plots"
                    ),
                    html.H4("More Info:", className="card-title"),
                    html.H5(
                        "(Hint: click one of the bins above to learn more)",
                        className="card-subtitle text-muted my-3",
                    ),
                    html.Div(
                        "", className="card-text", id="wiki_preliminary_plots_learnmore"
                    ),
                ]
            ),
            className="my-5",
        ),
        html.P(
            "To get a better feel for what the WikiPedia data looks like, you can look up the data for any substance you like below."
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Container(
                        [
                            dbc.Row(
                                dbc.Col(
                                    children="",
                                    id="wikipage_title",
                                ),
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Label("Choose which page to view:"), width=4
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="wikipage_select_dropdown",
                                            options=[
                                                {"label": i.title(), "value": i}
                                                for i in all_names_and_synonyms
                                            ],
                                            value="caffeine",
                                            placeholder="Pheibut, caffeine, modafinil, ...",
                                        ),
                                        width=3,
                                    ),
                                ],
                                className="my-3",
                            ),
                            dbc.Row(id="wikipage_preview", children=[]),
                        ]
                    ),
                ]
            ),
            className="my-5",
        ),
        html.Hr(className="my-5"),
        html.H3("Reddit Posts"),
        html.P(
            children=[
                html.A(
                    href="https://www.reddit.com/r/Nootropics/", children="r/Nootropics"
                ),
                """
                is a community on Reddit where people share experiences, ask questions, and discuss everything about cognitive enhancers and supplements.
                The 
                """,
                html.A(
                    href="https://github.com/pushshift/api", children="Pushshift API"
                ),
                """ let us download all submissions that were ever made on the subreddit - that is over 108.000 posts. 
                Then, we used the names (and synonyms) found on wikipedia to detect mentions of nootropics in those posts. 
                Let's look at some metrics.""",
            ]
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Some Histograms", className="card-title"),
                    dcc.Graph(
                        figure=reddit_preliminary_plots, id="reddit_preliminary_plots"
                    ),
                    html.H4("More Info:", className="card-title"),
                    html.H5(
                        "(Hint: click one of the bins above to learn more)",
                        className="card-subtitle text-muted my-3",
                    ),
                    html.Div(
                        "",
                        className="card-text",
                        id="reddit_preliminary_plots_learnmore",
                    ),
                ]
            ),
            className="mt-5",
        ),
        html.P(
            "In order to analyze the posts we got from reddit, we had to find as many mentions of nootropics in those posts as possible.\
                If you're interested in learning more about how we did, feel free to check our notebook - the link is on the homepage.\
            This allowed us to get, for each substance, a list of all posts that metion it. Once more, you can look at the data for any substance you like below."
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Container(
                        [
                            dbc.Row(
                                dbc.Col(
                                    children="",
                                    id="reddit_substance_title",
                                ),
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Label("Choose substance to view data for:"),
                                        width=4,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="reddit_substance_select_dropdown",
                                            options=[
                                                {"label": i.title(), "value": i}
                                                for i in all_names_and_synonyms
                                            ],
                                            value="caffeine",
                                            placeholder="Phenibut, caffeine, modafinil, ...",
                                        ),
                                        width=3,
                                    ),
                                ],
                                className="my-3",
                            ),
                            dbc.Row(id="reddit_substance_preview", children=[]),
                        ]
                    ),
                ]
            ),
            className="my-5",
        ),
    ]
)


@app.callback(
    Output("wiki_preliminary_plots_learnmore", "children"),
    Input("wiki_preliminary_plots", "clickData"),
)
def display_hover_data(clickdata):
    children = []
    clicked_plot = clickdata["points"][0]["curveNumber"]
    # return str(clickdata)
    selected_bucket_pages = get_name_by(clickdata["points"][0]["pointNumbers"][:5])
    if clicked_plot == 0:
        children.append(
            html.P(
                "This is the page length, in characters. Around half of the pages are very short, with less than 1.000 characters, but there are a few very long ones that have more than 60.000 characters."
            )
        )
        tables = [
            make_table_from_items(
                get_top("length", 5), "Longest Pages (n. of characters)"
            ),
            make_table_from_items(
                get_top("length", 5, reverse=True), "Shortest Pages (n. of characters)"
            ),
        ]
    elif clicked_plot == 1:
        children.append(
            html.P(
                "This is the count of links <b> towards other nootropics <b> that were found in each page. The amount of links is slightly more spread out, although the vast majority of pages as three or less links towards other nootropics. It's worth noting that 364 pages have no outgoing links at all."
            )
        )
        tables = [
            make_table_from_items(get_top("links", 5), "Pages with most links"),
            make_table_from_items(
                get_top("links", 5, reverse=True), "Pages with fewest links"
            ),
        ]
    elif clicked_plot == 2:
        children.append(
            html.P(
                "Synonyms were extracted by looking at which pages redirect to this page: if, for instance, <i> Vitamin B12 </i> redirects to <i> Cobalamin </i>, we can use that information to map all text mentions of the former to the latter page. \
                Once again, the number of synonyms per page is very skewed - more than a third of all pages have either one or no synonyms."
            )
        )
        tables = [
            make_table_from_items(get_top("synonyms", 5), "Pages with most synonyms"),
            make_table_from_items(
                get_top("synonyms", 5, reverse=True), "Pages with fewest synonyms"
            ),
        ]
    elif clicked_plot == 3:
        children.append(
            html.P(
                "Finally, all pages on wikipedia are part of one or more categories. Interestingly, here the distribution is smoother: there are actually no pages at all that have no categories, and it looks like most pages have approx. 5 categories."
            )
        )
        tables = [
            make_table_from_items(
                get_top("categories", 5), "Pages with most categories"
            ),
            make_table_from_items(
                get_top("categories", 5, reverse=True), "Pages with fewest categories"
            ),
        ]

    children.append(
        html.P(
            f"Some pages in the selected bin include: {', '.join([i.title() for i in selected_bucket_pages])}"
        )
    )

    children.append(
        dbc.Container(children=dbc.Row([dbc.Col(tables[0]), dbc.Col(tables[1])]))
    )

    return children


@app.callback(
    Output("reddit_preliminary_plots_learnmore", "children"),
    Input("reddit_preliminary_plots", "clickData"),
)
def display_hover_data(clickdata):
    children = []
    clicked_plot = clickdata["points"][0]["curveNumber"]
    # return str(clickdata)
    # selected_bucket_pages = get_name_by(clickdata["points"][0]["pointNumbers"][:5])
    if clicked_plot == 0:
        children.append(
            html.P(
                'The post length, in characters. Like on wikipedia, the distribution is very skewed \
                    - more than 10.000 posts are less than 30 characters long. \
                    As you can see from following the links in the table below, \
                    most of the  "short" posts are actually posts that have been removed. \
                    This initially created problems for our analysis, as we weren\'t aware\
                    of it, so we had to filter out many of those posts. '
            )
        )
        tables = [
            make_table_from_items(
                get_top_posts("length", amount=5, reverse=True),
                "Longest posts (n. of characters)",
            ),
            make_table_from_items(
                get_top_posts("length", amount=5),
                "Shortest posts (n. of characters)",
            ),
        ]
    elif clicked_plot == 1:
        children.append(
            html.P(
                children=[
                    "The distribution of the number of mentions of nootropics that were found in each post. \
                Again, very skewed, with almost half of all post having no mentions at all, and around a \
                third having only one mention. Since the relations between nootropics can only be extracted \
                when two or more substances are mentionned, this means that there are only around 25.000 posts that are effectively used in the analysis.\
                As you can see from looking at the posts with most links, they are almost all ",
                    html.Em("lists"),
                    " rather than actual posts that mention many substances.\
                This also caused a lot of noise, so we filtered out posts that mention more than a certain threshold of substances.",
                ]
            )
        )
        tables = [
            make_table_from_items(
                get_top_posts("mentions", amount=5, reverse=True),
                "Posts with most mentions",
            ),
            make_table_from_items(
                get_top_posts("mentions", amount=5),
                "Posts with fewest mentions",
            ),
        ]

    children.append(
        dbc.Container(children=dbc.Row([dbc.Col(tables[0]), dbc.Col(tables[1])]))
    )

    return children


@app.callback(
    [Output("wikipage_title", "children"), Output("wikipage_preview", "children")],
    Input("wikipage_select_dropdown", "value"),
)
def show_wiki_page(value):
    title, children = wiki_page(value)

    return [title, children]


@app.callback(
    [
        Output("reddit_substance_title", "children"),
        Output("reddit_substance_preview", "children"),
    ],
    Input("reddit_substance_select_dropdown", "value"),
)
def show_reddit_substance(value):
    title, children = reddit_substance(value)

    return [title, children]