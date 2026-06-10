"""
System Flow Demonstration — vougeabulary
Lead: Harman (Backend — Core API)

This script demonstrates the complete request-response cycle
for outfit recommendations, exactly as it happens in the web app.
Run: python system_flow.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from clothing_item import ClothingItem, Category, Occasion, Weather, Wardrobe
from recommendation_engine import RecommendationEngine
from database import get_all_items
from style_profiles import get_style, shopping_links


def simulate_request(temp: int, occasion: str, rain: bool):
    """Simulate a POST /api/recommend request."""

    print(f"\n{'='*54}")
    print(f"  REQUEST  -->  POST /api/recommend")
    print(f"  Body: {{ temp: {temp}, occasion: '{occasion}', rain: {rain} }}")
    print(f"{'='*54}")

    # Step 1: Load wardrobe (database layer)
    raw_items = get_all_items()
    print(f"\n[1] Loaded {len(raw_items)} items from wardrobe.json")

    # Step 2: Convert to engine objects (integration layer)
    wardrobe = Wardrobe()
    for i in raw_items:
        try:
            wardrobe.add_item(ClothingItem(
                item_id=i['id'], name=i['name'],
                category=Category(i['category']),
                color=i['color'],
                occasions=[Occasion(o) for o in i['occasions']],
                weather_suitability=[Weather(w) for w in i['weather']],
                is_clean=i.get('is_clean', True)
            ))
        except Exception:
            pass
    print(f"[2] Converted to {len(wardrobe.items)} ClothingItem objects")

    # Step 3: Run AI recommendation engine
    engine  = RecommendationEngine(wardrobe)
    results = engine.recommend(
        temp_celsius=temp,
        occasion=Occasion(occasion),
        is_raining=rain,
        top_n=3
    )
    print(f"[3] AI engine generated {len(results)} outfit(s)")

    # Step 4: Serialize to JSON (response format)
    print(f"\n[4] RESPONSE  -->  200 OK")
    print(f"  Body: {{ outfits: [...] }}\n")

    for idx, outfit in enumerate(results, 1):
        print(f"  Outfit #{idx}  (score: {outfit.score}/100)")
        for role, item in [("Top/Dress", outfit.top), ("Bottom", outfit.bottom),
                           ("Outerwear", outfit.outerwear), ("Shoes", outfit.shoes)]:
            if item:
                print(f"    {role:<10} : {item.name} ({item.color})")
    print()


def simulate_shop_request(style_key: str):
    """Simulate a GET /api/shop/<style> request."""
    print(f"\n{'='*54}")
    print(f"  REQUEST  -->  GET /api/shop/{style_key}")
    print(f"{'='*54}")
    profile = get_style(style_key)
    links   = shopping_links(style_key)
    print(f"\n  Style:       {profile['name']}")
    print(f"  Tagline:     {profile['tagline']}")
    print(f"  Colors:      {', '.join(profile['colors'][:3])}")
    print(f"  Brands:      {', '.join(profile['brands'][:3])}")
    print(f"  Shop links:  {len(links)} search terms, 4 platforms each")
    print(f"\n  First link set:")
    first = links[0]
    print(f"    Term:      {first['term']}")
    print(f"    Google:    {first['google']}")
    print(f"    ASOS:      {first['asos']}")
    print()


if __name__ == '__main__':
    print("\nvougeabulary — System Flow Demonstration")
    print("Harman — Backend Core API\n")

    simulate_request(temp=28, occasion='casual', rain=False)
    simulate_request(temp=14, occasion='work',   rain=False)
    simulate_request(temp=5,  occasion='formal', rain=False)
    simulate_shop_request('kawaii')
    simulate_shop_request('streetwear')
