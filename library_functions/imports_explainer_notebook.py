# %%

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config
