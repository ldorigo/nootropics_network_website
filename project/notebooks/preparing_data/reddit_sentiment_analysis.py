# %%

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

lf.calculate_sentiment_reddit()
# %%
