from fastapi import FastAPI, Query
import json

app = FastAPI()

# Load ads from file
with open("ads.json", "r") as f:
    ads = json.load(f)

@app.get("/ads")
def get_ads(
    game: str | None = None,
    advertiser: str | None = None,
    category: str | None = None,
    network: str | None = None
):
    """Return ads filtered by optional query parameters"""
    results = ads
    if game:
        results = [a for a in results if a["game"] == game]
    if advertiser:
        results = [a for a in results if a["advertiser"] == advertiser]
    if category:
        results = [a for a in results if a["category"] == category]
    if network:
        results = [a for a in results if a["network"] == network]
    return results

@app.get("/ads/stats")
def get_ad_stats(groupBy: str = Query(..., regex="^(advertiser|category|game)$")):
    """Return aggregated ad counts grouped by advertiser, category, or game"""
    counts = {}
    for ad in ads:
        key = ad[groupBy]
        counts[key] = counts.get(key, 0) + 1
    return [{"key": k, "count": v} for k, v in counts.items()]
