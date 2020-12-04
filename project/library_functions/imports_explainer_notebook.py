# %%
import numpy as np
import pandas as pd
import warnings
import wojciech as w

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf

try:
    from library_functions.config import Config
except ModuleNotFoundError:
    from project.library_functions.config import Config

warnings.filterwarnings('ignore')
