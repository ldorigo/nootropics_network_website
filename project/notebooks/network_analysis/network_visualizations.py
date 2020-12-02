# %%
from fa2 import ForceAtlas2
from networkx.readwrite.adjlist import read_adjlist
import networkx as nx
from config import Config
import wojciech as w
import library_functions as lf
import importlib

#%%
# graph_reddit : nx.Graph
# graph_wiki : nx.Graph
# graph_reddit = nx.readwrite.gpickle.read_gpickle(Config.Path.reddit_gcc)
# graph_wiki = nx.readwrite.gpickle.read_gpickle(Config.Path.wiki_gcc)

graph_reddit = lf.create_graph_reddit(
    max_drugs_in_post=6,
    min_edge_occurrences_to_link=2,
    # alternative_path="./private_data/reddit_data_with_NER.json",
)
graph_wiki = lf.create_graph_wiki().to_undirected()


graph_reddit = w.graph.largest_connected_component(graph_reddit)
# %%


(
    reddit_graph,
    reddit_partition,
    wiki_graph,
    wiki_partition,
) = lf.assign_louvain_communities(reddit_graph=graph_reddit, wiki_graph=graph_wiki)

positions_reddit = lf.get_fa2_layout(graph=graph_reddit, edge_weight_attribute="count")
# %%
importlib.reload(lf.plotly_draw)
from library_functions import plotly_draw

# plotly_draw.draw_graph_plotly(
#     graph = graph_wiki,
#     positions=positions_wiki
# )
# %%
plotly_draw.draw_graph_plotly(
    graph=graph_reddit,
    positions=positions_reddit,
    node_size_attribute="degree",
    edge_weight_attribute="count",
)

# %%
plotly_draw.draw_graph_plotly(
    graph=graph_reddit,
    positions=positions_reddit,
    node_size_attribute="degree",
    node_color_attribute="louvain_community_reddit",
)
# %%
plotly_draw.draw_graph_plotly(
    graph=graph_wiki,
    positions=positions_wiki,
    node_size_attribute="degree",
    node_color_attribute="louvain_community_wiki",
)
# %%
