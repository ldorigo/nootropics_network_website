# %%

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf
import matplotlib.pyplot as plt
import numpy as np
import wojciech as w

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config

#%%
reddit_data = lf.load_data_reddit()

content_length = [len(post["content"]) for post in reddit_data.values()]

figure, axes = w.empty_figure()

axes.hist(content_length, bins=np.linspace(0, 100, 101))

plt.show()

#%%
nonempty_posts_less_than_25 = [
    (post["content"], post["matches"])
    for post in reddit_data.values()
    if len(post["content"]) < 25
]

posts_polarity_0 = [
    (post["content"], len(post["content"]), post["matches"])
    for post in reddit_data.values()
    if post["polarity"] == 0
]
