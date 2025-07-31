import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
from data_loader import get_latest_df

import pandas as pd
#from app.data_loader import get_latest_df
df = get_latest_df()  # however you load your data
print(df.columns)
print(df.info())
print(df.head(10))
print(df.tail(10))
print(df.isnull().sum())

"""
print(df.info())
print(df.head(10))
print(df.tail(10))

# Check for missing data
print(df.isnull().sum())

# Check for continuous date index
print(df.index)
print(df.index.min(), df.index.max(), len(df))

# Check for duplicate dates
print(df.index.duplicated().sum())"""
#print(df.columns)
