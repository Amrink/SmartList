import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def google_nearby_restaurants(lat, lng, radius_meters, cuisine_keyword=None, min_price=None, max_price=None, open_now=False):
    if not GOOGLE_API_KEY:
        raise RuntimeError("Missing GOOGLE_MAPS_API_KEY in .env")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_API_KEY,
        "location": f"{lat},{lng}",
        "radius": radius_meters,
        "type": "restaurant",
    }

    if open_now:
        params["opennow"] = "true"
    if cuisine_keyword:
        params["keyword"] = cuisine_keyword
    if min_price is not None:
        params["minprice"] = int(min_price)
    if max_price is not None:
        params["maxprice"] = int(max_price)

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results", [])

    # rank by rating then number of reviews
    results.sort(
        key=lambda p: (float(p.get("rating", 0.0)), int(p.get("user_ratings_total", 0))),
        reverse=True
    )

    top = []
    for p in results[:3]:
        top.append({
            "name": p.get("name"),
            "rating": p.get("rating"),
            "ratings_total": p.get("user_ratings_total"),
            "price_level": p.get("price_level"),
            "address": p.get("vicinity"),
            "place_id": p.get("place_id"),
        })
    return top
