"""
Code testing
"""

import pandas as pd


combined = pd.concat(
    [pd.read_csv(f"Location/2018/{i}.csv", index_col=False) for i in range(0, 7)]
)
combined = combined[["teamNumber", "location", "latitude", "longitude"]]
combined.to_csv("Location/2018/2018Location.csv", index=False)
