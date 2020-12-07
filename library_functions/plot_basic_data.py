import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf


def get_wiki_plots_figure():
    pages_distribution = make_subplots(
        rows=4,
        cols=1,
        subplot_titles=(
            "Length (N. of Characters)",
            "Amount of Links",
            "Amount of Synonyms (redirects)",
            "Amount of categories",
        ),
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_page_lengths(),
            hovertemplate=f"Length (N. of Characters):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=1,
        col=1,
    )
    # pages_distribution.update_xaxes(, row=1, col=1)
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_links(),
            hovertemplate=f"Amount of Links:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=2,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_synonyms(),
            hovertemplate=f"Amount of Synonyms (redirects):  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=3,
        col=1,
    )
    pages_distribution.add_trace(
        go.Histogram(
            x=lf.get_number_of_categories(),
            hovertemplate=f"Amount of categories:  %{{x}} <br>Number of pages:  %{{y}}",
        ),
        row=4,
        col=1,
    )

    pages_distribution.update_layout(
        # margin={"l": 20, "r": 20, "t": 25, "b": 25},
        xaxis={},
        yaxis={},
        showlegend=False,
        clickmode="event+select",
        height=650,
    )
    return pages_distribution


def get_reddit_plots_figure():
    posts_distribution = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Length (N. of Characters)",
            "Amount of Nootropics Mentions",
        ),
    )
    posts_distribution.add_trace(
        go.Histogram(
            x=lf.get_post_lengths(),
            hovertemplate=f"Length (N. of Characters):  %{{x}} <br>Number of posts:  %{{y}}",
        ),
        row=1,
        col=1,
    )
    # pages_distribution.update_xaxes(, row=1, col=1)
    posts_distribution.add_trace(
        go.Histogram(
            x=lf.get_n_of_matches_per_post(),
            hovertemplate=f"Amount of mentions:  %{{x}} <br>Number of posts:  %{{y}}",
        ),
        row=2,
        col=1,
    )

    posts_distribution.update_layout(
        # margin={"l": 20, "r": 20, "t": 25, "b": 25},
        xaxis={},
        yaxis={},
        showlegend=False,
        clickmode="event+select",
        height=650,
    )
    return posts_distribution