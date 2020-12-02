import networkx as nx

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf


def create_graph_wiki():
    wiki_data = lf.load_data_wiki()
    substance_names = lf.load_substance_names()

    g_wiki = nx.DiGraph()
    g_wiki.add_nodes_from(substance_names, categories=[])

    # Assign categories from Wikipedia to drugs as well as text contents and url
    for index_drug, drug in enumerate(wiki_data["name"]):
        if drug in g_wiki.nodes:
            g_wiki.nodes[drug]["categories"] = wiki_data["categories"][index_drug]
            g_wiki.nodes[drug]["content"] = wiki_data["content"]
            g_wiki.nodes[drug]["url"] = wiki_data["url"]

    for index_drug, drug in enumerate(wiki_data["name"]):
        if drug not in g_wiki.nodes:
            continue

        for drug_to_link_to, n_links in wiki_data["links"][index_drug].items():
            if drug_to_link_to in g_wiki.nodes:
                g_wiki.add_edge(drug, drug_to_link_to, count=n_links)

    return g_wiki
