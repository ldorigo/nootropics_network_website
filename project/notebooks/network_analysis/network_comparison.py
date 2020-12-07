# %%
from library_functions.initialize_explainer_notebook import *

# %% Create graphs
g_wiki = lf.create_graph_wiki()
g_reddit = lf.create_graph_reddit()
g_reddit_post_length_limit = lf.create_graph_reddit(
    max_drugs_in_post=10, min_content_length_in_characters=25
)

g_reddit_max_10 = lf.create_graph_reddit(max_drugs_in_post=10)
g_reddit_min_3_links = lf.create_graph_reddit(min_edge_occurrences_to_link=3)

g_reddit_chosen = lf.create_graph_reddit(
    max_drugs_in_post=10,
    min_edge_occurrences_to_link=3,
    min_content_length_in_characters=25,
)

# Positive sentiment
conditions_positive = {"polarity": lambda x: x > 0.13}
g_reddit_positive = lf.create_graph_reddit(
    max_drugs_in_post=10,
    min_edge_occurrences_to_link=3,
    min_content_length_in_characters=25,
    conditional_functions_dict=conditions_positive,
)

# Negative sentiment
conditions_negative = {"polarity": lambda x: x < 0.13}
g_reddit_negative = lf.create_graph_reddit(
    max_drugs_in_post=10,
    min_edge_occurrences_to_link=3,
    min_content_length_in_characters=25,
    conditional_functions_dict=conditions_negative,
)


# %% Plot comparison of attribute distributions
graphs = [
    g_reddit,
    g_reddit_max_10,
    g_reddit_min_3_links,
    g_reddit_post_length_limit,
    # g_reddit_positive,
    # g_reddit_negative
]

graph_names = [
    "Reddit Raw",
    "Max 10 drugs in post",
    "Min 3 occurrences for link",
    "Only posts with 25+ characters"
    # 'Reddit positive',
    # 'Reddit negative'
]

axess = lf.plot_comparison_of_attribute_distributions(
    graphs,
    graph_names=graph_names,
    attribute_name="polarity_weighted",
    attribute_parent="edge",
    attribute_function=None,
    attribute_function_name="",
    as_probability_distribution=False,
    bins=np.linspace(-1, 1, 201),
    show=False,
)

axess[0].set_xlim((-0.5, 0.5))
plt.show()

# %% Plot distribution of values of one instance (node or edge)
graphs = [g_reddit, g_reddit_max_10, g_reddit_min_3_links, g_reddit_post_length_limit]

graph_names = [
    "Reddit Raw",
    "Max 10 drugs in post",
    "Min 3 occurrences for link",
    "Only posts with 25+ characters",
]

instance = "node"
instance_label = "caffeine"
attribute_name = "polarity"

w.graph.plot_distribution_of_attribute_of_1_instance(
    graphs,
    instance=instance,
    instance_label=instance_label,
    attribute_name=attribute_name,
    graph_names=graph_names,
)

# %% Plot degree distribution summary
graphs_to_show = [g_reddit, g_wiki, w.graph.erdos_renyi_like(g_reddit)]
graph_names = ["Reddit", "Wiki", "Random like Reddit"]
graph_colors = ["red", "blue", "green"]

w.graph.plot_degree_distribution_summary(
    graphs_to_show,
    graph_names=graph_names,
    graph_colors=graph_colors,
    x_lim_lin=(-2, 100),
    x_lim_log=(0.9, 1000),
)

# %% Most central nodes Wiki
centrality_measures = \
    ["degree", "in-degree", "out-degree", "betweenness", "eigenvector"]

most_central_nodes_wiki = \
    w.graph.most_central_nodes(g_wiki, centrality_measures, n=10, printout=True)

# %% Most central nodes Reddit
for centrality in ["degree", "betweenness", "eigenvector"]:
    w.graph.most_central_nodes(g_reddit, centrality, n=10, printout=True)

# %% In vs out degree Wiki
w.graph.plot_in_vs_out_degree(g_wiki, plot_type="heatmap", colormap_norm="log")
plt.show()

# %% Force Atlas plot Wiki
# w.graph.plot_force_atlas_2(w.graph.remove_isolates(g_wiki),
#                            node_size='by degree',
#                            node_color=np.array([[0, 0, 1, 0.5]]),
#                            edge_color=np.array([[0, 0, 0, 0.1]]),
#                            alpha=None,
#                            iterations=100,
#                            outboundAttractionDistribution=True)
# plt.show()


# %% Degree stats
graphs = [g_reddit, g_reddit_positive, g_reddit_negative]
graph_names = ["Reddit", "Reddit Positive", "Reddit Negative"]

degree_stats = dict()
for graph, graph_name in zip(graphs, graph_names):
    print(f"\n{graph_name}:")
    degree_stats[graph_name] = w.graph.degree_statistics(graph, printout=True)

# %% Most central nodes in different Reddit Graphs
graphs = [g_reddit, g_reddit_positive, g_reddit_negative]
graph_names = ["Reddit", "Reddit Positive", "Reddit Negative"]
centralities = ["degree"]

for graph, graph_name in zip(graphs, graph_names):
    print(f"\n{graph_name}:")
    for centrality in centralities:
        w.graph.most_central_nodes(graph, centrality, n=10, printout=True)

# %% Save graphs to pickle
nx.readwrite.gpickle.write_gpickle(g_reddit, Config.Path.reddit_graph)
nx.readwrite.gpickle.write_gpickle(g_wiki, Config.Path.wiki_digraph)

# %% Let's look at the GCC's and undirected graphs for the following.

gcc_wiki_dir = w.graph.largest_connected_component(g_wiki)
gcc_reddit = w.graph.largest_connected_component(g_reddit)

# %%
gcc_wiki = gcc_wiki_dir.to_undirected()

nx.readwrite.gpickle.write_gpickle(gcc_reddit, Config.Path.reddit_gcc)
nx.readwrite.gpickle.write_gpickle(gcc_wiki, Config.Path.wiki_gcc)

# %% Find Reddit posts with most substances
# reddit_data = lf.load_data_reddit()
#
# max_matches = 0
# label_max = ''
# for post_label, post in reddit_data.items():
#     if len(post['matches']) > max_matches:
#         max_matches = len(post['matches'])
#         label_max = post_label
#
# post_with_most_matches = reddit_data[label_max]
