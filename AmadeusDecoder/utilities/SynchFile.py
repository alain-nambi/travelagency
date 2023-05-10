import os
import pandas as pd

from io import BytesIO

def retrieve_file(path):
    df = pd.read_csv(path)
    return df
