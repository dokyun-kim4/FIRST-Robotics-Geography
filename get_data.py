"""
Imports a list of all FRC teams from 2023 season
"""

import requests as rq


URL = "https://frc-api.firstinspires.org/v3.0/2023/teams"
TOKEN = "Basic dkim4:dd3338ba-b90d-473d-96bc-ead9bd88e480"
HEADER = {
    "Authorization": TOKEN,
    "Is-Modified-Since": None,
}

data = rq.get(
    URL,
    headers=HEADER,
    timeout=10,
)
print(data.status_code)
print(data.reason)


# url = "https://frc-api.firstinspires.org/v3.0/"
# data = rq.get(url, timeout=5)
# print(data.text)
