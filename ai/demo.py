"""
vougeabulary — AI Recommendation Demo
Run:  python demo.py
"""
from clothing_item import ClothingItem, Category, Occasion, Weather, Wardrobe
from recommendation_engine import RecommendationEngine


# ── Build a sample wardrobe ────────────────────────────────────────────────────

wardrobe = Wardrobe()

wardrobe.add_item(ClothingItem("t1", "White Linen Shirt",   Category.TOP,       "white",    [Occasion.CASUAL, Occasion.WORK],          [Weather.HOT, Weather.WARM]))
wardrobe.add_item(ClothingItem("t2", "Black Turtleneck",    Category.TOP,       "black",    [Occasion.CASUAL, Occasion.FORMAL, Occasion.WORK], [Weather.COOL, Weather.COLD]))
wardrobe.add_item(ClothingItem("t3", "Navy Polo",           Category.TOP,       "navy",     [Occasion.CASUAL, Occasion.WORK],          [Weather.WARM, Weather.COOL]))
wardrobe.add_item(ClothingItem("t4", "Pink Blouse",         Category.TOP,       "pink",     [Occasion.PARTY, Occasion.CASUAL],         [Weather.WARM, Weather.HOT]))

wardrobe.add_item(ClothingItem("b1", "Blue Jeans",          Category.BOTTOM,    "blue",     [Occasion.CASUAL],                         [Weather.WARM, Weather.COOL, Weather.COLD]))
wardrobe.add_item(ClothingItem("b2", "Black Trousers",      Category.BOTTOM,    "black",    [Occasion.FORMAL, Occasion.WORK],          [Weather.COOL, Weather.COLD, Weather.WARM]))
wardrobe.add_item(ClothingItem("b3", "Beige Chinos",        Category.BOTTOM,    "beige",    [Occasion.CASUAL, Occasion.WORK],          [Weather.WARM, Weather.COOL]))
wardrobe.add_item(ClothingItem("b4", "Olive Cargo Pants",   Category.BOTTOM,    "olive",    [Occasion.CASUAL, Occasion.SPORT],         [Weather.COOL, Weather.WARM]))

wardrobe.add_item(ClothingItem("d1", "Red Floral Dress",    Category.DRESS,     "red",      [Occasion.PARTY, Occasion.CASUAL],         [Weather.HOT, Weather.WARM]))
wardrobe.add_item(ClothingItem("d2", "Navy Midi Dress",     Category.DRESS,     "navy",     [Occasion.FORMAL, Occasion.WORK],          [Weather.WARM, Weather.COOL]))

wardrobe.add_item(ClothingItem("s1", "White Sneakers",      Category.SHOES,     "white",    [Occasion.CASUAL, Occasion.SPORT],         [Weather.HOT, Weather.WARM, Weather.COOL]))
wardrobe.add_item(ClothingItem("s2", "Black Heels",         Category.SHOES,     "black",    [Occasion.FORMAL, Occasion.PARTY, Occasion.WORK], [Weather.WARM, Weather.COOL]))
wardrobe.add_item(ClothingItem("s3", "Brown Loafers",       Category.SHOES,     "brown",    [Occasion.CASUAL, Occasion.WORK],          [Weather.WARM, Weather.COOL, Weather.COLD]))
wardrobe.add_item(ClothingItem("s4", "Black Boots",         Category.SHOES,     "black",    [Occasion.CASUAL, Occasion.FORMAL],        [Weather.COLD, Weather.COOL, Weather.RAINY]))

wardrobe.add_item(ClothingItem("o1", "Black Wool Coat",     Category.OUTERWEAR, "black",    [Occasion.FORMAL, Occasion.CASUAL, Occasion.WORK], [Weather.COLD, Weather.COOL]))
wardrobe.add_item(ClothingItem("o2", "Beige Trench Coat",   Category.OUTERWEAR, "beige",    [Occasion.CASUAL, Occasion.WORK],          [Weather.COOL, Weather.RAINY]))
wardrobe.add_item(ClothingItem("o3", "Navy Rain Jacket",    Category.OUTERWEAR, "navy",     [Occasion.CASUAL, Occasion.SPORT],         [Weather.RAINY, Weather.COOL]))


# ── Run recommendations ────────────────────────────────────────────────────────

engine = RecommendationEngine(wardrobe)

scenarios = [
    {"label": "Sunny day, 32°C — Casual outing",  "temp": 32, "occasion": Occasion.CASUAL,  "rain": False},
    {"label": "Chilly office day, 15°C",           "temp": 15, "occasion": Occasion.WORK,    "rain": False},
    {"label": "Rainy evening, 13°C — Party",       "temp": 13, "occasion": Occasion.PARTY,   "rain": True},
    {"label": "Cold formal event, 5°C",            "temp":  5, "occasion": Occasion.FORMAL,  "rain": False},
]

for scenario in scenarios:
    print(f"\n{'='*55}")
    print(f"  {scenario['label']}")
    print(f"{'='*55}")

    results = engine.recommend(
        temp_celsius=scenario["temp"],
        occasion=scenario["occasion"],
        is_raining=scenario["rain"],
        top_n=3,
    )

    if not results:
        print("  No suitable outfits found.")
    else:
        for rank, outfit in enumerate(results, 1):
            print(f"\n  Outfit #{rank}")
            print(outfit.display())
