from utils.data import (
    all_names_and_synonyms,
    synonym_mapping,
    graph_reddit,
    graph_wiki_directed,
    reddit_data,
)
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def wiki_page(substance_name: str):
    name = synonym_mapping[substance_name]
    nodedata = graph_wiki_directed.nodes[name]
    incoming = graph_wiki_directed.in_degree[name]
    outgoing = graph_wiki_directed.out_degree[name]
    synonyms = [i for i in synonym_mapping if synonym_mapping[i] == name]
    table = dbc.Table(
        children=[
            html.Thead(
                html.Tr(
                    html.Th(
                        colSpan=2,
                        children="Page Properties",
                        style={"text-align": "center"},
                    )
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Th("Length (in characters)"),
                            html.Td(f"{len(nodedata['content'])}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Links to other pages"),
                            html.Td(f"{outgoing}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Links from other pages"),
                            html.Td(f"{incoming}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Amount of categories"),
                            html.Td(f"{len(nodedata['categories'])}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Amount of synonyms"),
                            html.Td(f"{len(synonyms)}"),
                        ]
                    ),
                ]
            ),
        ],
        borderless=True,
        striped=True,
        hover=True,
    )
    titlechildren = []
    titlechildren.append(
        html.H5(f"Wikipedia Entry: {name}".title(), className="card-title")
    )
    if name != substance_name:
        titlechildren.append(
            html.P(
                html.Em(f"(redirected from: {substance_name})"), className="text-muted"
            )
        )

    preview_children = [
        html.H6("Preview:"),
        html.P(nodedata["content"][:800] + "..."),
    ]

    categories_text = "; ".join([i.title() for i in nodedata["categories"]][:10])
    if len(nodedata["categories"]) > 10:
        categories_text += f", and {len(nodedata['categories']) - 10} more."

    if nodedata["categories"]:
        preview_children += [
            html.H6("This page has the following categories:"),
            html.P(categories_text),
        ]
    else:
        preview_children.append(html.H6("This page has no categories."))

    redirects_text = "; ".join([i.title() for i in synonyms][:10])
    if len(synonyms) > 10:
        redirects_text += f", and {len(synonyms) - 10} more."

    if synonyms:
        preview_children += [
            html.H6("This page has the following synonyms (redirects):"),
            html.P(redirects_text),
        ]
    else:
        preview_children.append(html.H6("This page has no synonyms."))

    preview_children.append(
        html.A(
            html.H6("Click here to view the page on WikiPedia."), href=nodedata["url"]
        )
    )
    children = [
        dbc.Col(
            preview_children,
            width=8,
        ),
        dbc.Col(children=table, width=4),
    ]

    return titlechildren, children


def reddit_substance(substance_name):
    name = synonym_mapping[substance_name]
    nodedata = graph_reddit.nodes[name]
    titlechildren = []
    titlechildren.append(
        html.H5(f"Reddit Posts for: {name}".title(), className="card-title")
    )
    if name != substance_name:
        titlechildren.append(
            html.P(
                html.Em(f"(Resolved from: {substance_name})"), className="text-muted"
            )
        )

    n_links = graph_reddit.degree(name)
    total_length = sum([len(i) for i in nodedata["contents"]])
    edge_counts = sorted(
        graph_reddit.edges("caffeine", data="count"), key=lambda x: x[2]
    )

    top_edges_rows = []
    for _, to, count in edge_counts[:5]:
        top_edges_rows.append(
            html.Tr(
                [
                    html.Th(to.title()),
                    html.Td(count),
                ]
            ),
        )

    top_edges_table = children = (
        [
            html.Thead(
                html.Tr(
                    html.Th(
                        colSpan=2,
                        children="Substances most often mentioned with this one",
                        style={"text-align": "center"},
                    )
                )
            ),
            html.Tbody(top_edges_rows),
        ],
    )

    table = dbc.Table(
        children=[
            html.Thead(
                html.Tr(
                    html.Th(
                        colSpan=2,
                        children="Node Properties",
                        style={"text-align": "center"},
                    )
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Th("Number of posts"),
                            html.Td(f"{len(nodedata['ids'])}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Links to other substances"),
                            html.Td(f"{n_links}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Total length of all posts (in characters)"),
                            html.Td(f"{total_length}"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Th("Average post length (in characters)"),
                            html.Td(f"{total_length/len(nodedata['ids'])}"),
                        ]
                    ),
                ]
            ),
        ],
        borderless=True,
        striped=True,
        hover=True,
    )

    preview_children = [html.H6("Some example posts:")]

    for post_id in nodedata["ids"][:5]:
        preview_children += [html.P([html.B("Title: "), reddit_data[post_id]["title"]])]

        contents_paragraph = [html.B("Contents: ")]

        if reddit_data[post_id]["content"]:
            post_text = reddit_data[post_id]["content"][:200]
            if len(reddit_data[post_id]["content"]) > 200:
                post_text += " ..."
        else:
            post_text = "[no content]"
        contents_paragraph.append(post_text)

        preview_children += [html.P(contents_paragraph)]
        preview_children += [
            html.A(
                "View on reddit",
                href=f"https://www.reddit.com/r/Nootropics/comments/{post_id}",
            )
        ]
    children = [
        dbc.Col(
            preview_children,
            width=6,
        ),
        dbc.Col(children=[table], width=4),
    ]
    return [titlechildren, children]
