# %%
import json

try:
    import library_functions as lf
except ModuleNotFoundError:
    import project.library_functions as lf


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import powerlaw
import wojciech as w

try:
    from config import Config
except ModuleNotFoundError:
    from project.config import Config
from fa2 import ForceAtlas2
from operator import itemgetter
from pandas_profiling import ProfileReport
from pathlib import Path