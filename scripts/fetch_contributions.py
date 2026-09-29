"""Fetch the last year of contributions from the GitHub GraphQL API."""

import json
import os
import pathlib
import urllib.request

USER = os.environ.get("GH_USER", "Hashim0011")
TOKEN = os.environ["GH_TOKEN"]
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "contributions.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req) as res:
    payload = json.load(res)

calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(calendar, indent=1))
print(f"{calendar['totalContributions']} contributions -> {OUT.name}")
