from pathlib import Path


class Config:
    class Path:

        # Project root
        project_root = Path(__file__).parent

        # Private data (not added to git to save space and bandwidth)
        private_data_folder = project_root / "private_data"

        # Shared data:
        shared_data_folder = project_root / "shared_data"

        dietary_supplements_category_tree_clean = (
            shared_data_folder / "dietary_supplements_category_tree_clean.json"
        )

        dietary_supplements_category_tree_raw = (
            shared_data_folder / "dietary_supplements_category_tree_raw.json"
        )

        full_category_tree_clean = shared_data_folder / "full_category_tree_clean.json"

        full_wiki_data = shared_data_folder / "full_wiki_data.json"

        psychoactive_category_tree_clean = (
            shared_data_folder / "psychoactive_category_tree_clean.json"
        )

        psychoactive_category_tree_raw = (
            shared_data_folder / "psychoactive_category_tree_raw.json"
        )

        reddit_data_with_NER = shared_data_folder / "reddit_data_with_NER.json"

        reddit_data_with_NER_and_sentiment = (
            shared_data_folder / "reddit_data_with_NER_and_sentiment.json"
        )

        substance_names = shared_data_folder / "substance_names.json"

        synonym_mapping = shared_data_folder / "synonym_mapping.json"

        contents_per_substance = shared_data_folder / "contents_per_substance.json"
        urls_per_substance = shared_data_folder / "urls_per_substance.json"

        posts_per_substance = shared_data_folder / "posts_per_substance.json"
        posts_per_link = shared_data_folder / "posts_per_link.json"
        # Wiki data:
        wiki_data_folder = shared_data_folder / "wikipedia_data"

        all_categories_to_names_mapping = (
            shared_data_folder / "all_categories_to_names_mapping.json"
        )

        wiki_mechanism_categories = (
            shared_data_folder / "wiki_mechanism_categories.json"
        )
        wiki_effect_categories = shared_data_folder / "wiki_effect_categories.json"
        # Graphs

        wiki_digraph = shared_data_folder / "wiki_digraph.gpickle"
        reddit_graph = shared_data_folder / "reddit_graph.gpickle"
        wiki_gcc = shared_data_folder / "wiki_gcc.gpickle"
        reddit_gcc = shared_data_folder / "reddit_gcc.gpickle"
        reddit_with_text = shared_data_folder / "reddit_with_textdata.gpickle"

    class Color:
        red = (1, 0, 0, 0.3)
        blue = (0, 0, 1, 0.3)
        black = (0, 0, 0, 0.6)
