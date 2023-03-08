"""
Code testing
"""
import json
import requests as rq
import pandas as pd

import data_functions as dfn
from data_functions import TOKEN, HEADER

CUTOFF = dfn.find_cutoff(dfn.read_text(dfn.build_url(2023, 1)))
print(CUTOFF)

test = []

for i in range(1, 73):
    print(i)
    url = dfn.build_url(2023, i)
    response = rq.request(
        "GET",
        url,
        auth=TOKEN,
        headers=HEADER,
        data={},
        timeout=10,
    )
    print(response.text)
    print("\n---------------------------------\n")
    # after_cut = dfn.trim_data(response.text)
    # test += after_cut

# print("Done")
# df = pd.DataFrame(test)
# df.to_csv("test.csv")

# All = []
# for i in range(1, 5):
#     All += dfn.extract_data_one_page(2023, i)

# df = pd.DataFrame(All)
# df.to_csv("test.csv")


# dfn.extract_data_all_pages(2019)
