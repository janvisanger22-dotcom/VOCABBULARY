# Vougeabulary — Recommendation Engine Design

## 1. Data Structure

### ClothingItem
Each item in the wardrobe is stored with these fields:

| Field                 | Type          | Example values                        |
|-----------------------|---------------|---------------------------------------|
| `item_id`             | string        | "t1"                                  |
| `name`                | string        | "White Linen Shirt"                   |
| `category`            | enum          | top, bottom, dress, outerwear, shoes  |
| `color`               | string        | "white", "navy", "beige"              |
| `occasions`           | list of enums | casual, formal, work, sport, party    |
| `weather_suitability` | list of enums | hot, warm, cool, cold, rainy          |
| `is_clean`            | boolean       | true / false                          |

### Outfit (output object)
| Field       | Type          |
|-------------|---------------|
| `top`       | ClothingItem  |
| `bottom`    | ClothingItem  |
| `shoes`     | ClothingItem  |
| `outerwear` | ClothingItem  |
| `score`     | float (0–100) |

---

## 2. Color Matching Rules

Colors are grouped into four tone families:

| Group    | Colors                                            |
|----------|---------------------------------------------------|
| Neutral  | black, white, grey, beige, navy, cream, camel     |
| Warm     | red, orange, yellow, pink, coral, burgundy        |
| Cool     | blue, green, purple, teal, mint, lavender         |
| Earth    | brown, olive, mustard, rust, tan, khaki           |

**Compatibility scores (0.0 = clash → 1.0 = perfect):**

| Pair              | Score |
|-------------------|-------|
| Neutral + Any     | 1.00  |
| Warm + Warm       | 0.80  |
| Cool + Cool       | 0.80  |
| Earth + Earth     | 0.85  |
| Warm + Earth      | 0.75  |
| Cool + Earth      | 0.70  |
| Warm + Cool       | 0.40  |

**Outfit score formula:**
```
score = color_score(top, bottom) × 50
      + color_score(top, shoes)  × 25
      + color_score(bottom, shoes) × 25
```
Maximum possible score = 100.

---

## 3. Recommendation Engine — Flowchart

```
┌─────────────────────────────────────────────────────┐
│                    USER INPUT                       │
│   temperature (°C)  |  occasion  |  raining? (y/n) │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│              STEP 1 — WEATHER MAPPING               │
│  temp ≥ 30°C        → HOT                          │
│  20°C ≤ temp < 30°C → WARM                         │
│  10°C ≤ temp < 20°C → COOL                         │
│  temp < 10°C        → COLD                         │
│  raining = yes      → RAINY (overrides all)        │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│          STEP 2 — FILTER WARDROBE                   │
│  For each category (top, bottom, dress, shoes,      │
│  outerwear):                                        │
│    Keep item if:                                    │
│      • weather IN item.weather_suitability          │
│      • occasion IN item.occasions                   │
│      • item.is_clean = true                         │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│        STEP 3 — BUILD OUTFIT COMBINATIONS           │
│                                                     │
│  FOR each top in filtered tops:                     │
│    FOR each bottom in filtered bottoms:             │
│      best_shoe = shoe with highest color score      │
│      outfit = { top, bottom, best_shoe }            │
│      outfit.score = calculate_score(outfit)         │
│      add outfit to candidates list                  │
│                                                     │
│  FOR each dress in filtered dresses:                │
│      best_shoe = shoe with highest color score      │
│      outfit = { dress, null, best_shoe }            │
│      outfit.score = calculate_score(outfit)         │
│      add outfit to candidates list                  │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│          STEP 4 — SCORE & RANK                      │
│  Sort candidates list by score (highest first)      │
│  Keep top 3 (or top N as configured)                │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│          STEP 5 — ADD OUTERWEAR (if needed)         │
│  IF weather is COOL, COLD, or RAINY:                │
│    For each top outfit:                             │
│      Pick outerwear with best color match to top    │
│      Attach to outfit                               │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│               OUTPUT — TOP OUTFITS                  │
│   Display ranked outfits with score to user         │
└─────────────────────────────────────────────────────┘
```

---

## 4. Pseudocode

```
FUNCTION recommend(temperature, occasion, is_raining):

    weather = map_weather(temperature, is_raining)

    tops      = filter(wardrobe, category=TOP,       weather, occasion)
    bottoms   = filter(wardrobe, category=BOTTOM,    weather, occasion)
    dresses   = filter(wardrobe, category=DRESS,     weather, occasion)
    shoes     = filter(wardrobe, category=SHOES,     weather, occasion)
    outerwear = filter(wardrobe, category=OUTERWEAR, weather, occasion)

    candidates = []

    FOR top IN tops:
        FOR bottom IN bottoms:
            best_shoe = MAX(shoes, by: color_score(top, shoe) + color_score(bottom, shoe))
            score     = color_score(top, bottom) × 50
                      + color_score(top, best_shoe)    × 25
                      + color_score(bottom, best_shoe) × 25
            candidates.ADD( Outfit(top, bottom, best_shoe, score) )

    FOR dress IN dresses:
        best_shoe = MAX(shoes, by: color_score(dress, shoe))
        score     = 50 + color_score(dress, best_shoe) × 50
        candidates.ADD( Outfit(dress, null, best_shoe, score) )

    candidates.SORT(by: score, order: descending)
    top_outfits = candidates[0..2]   // top 3

    IF weather IN {COOL, COLD, RAINY}:
        FOR outfit IN top_outfits:
            best_outer = MAX(outerwear, by: color_score(outfit.top, outer))
            outfit.outerwear = best_outer

    RETURN top_outfits


FUNCTION map_weather(temperature, is_raining):
    IF is_raining    → RETURN RAINY
    IF temp >= 30    → RETURN HOT
    IF temp >= 20    → RETURN WARM
    IF temp >= 10    → RETURN COOL
    ELSE             → RETURN COLD


FUNCTION color_score(item_a, item_b):
    group_a = get_color_group(item_a.color)
    group_b = get_color_group(item_b.color)
    RETURN compatibility_table[group_a][group_b]
```
