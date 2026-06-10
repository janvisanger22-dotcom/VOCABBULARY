# AI & Recommendation System — Technical Report
### vougeabulary | AI & Recommendation Lead: Samaira

---

## 1. Overview

The AI component of vougeabulary is a rule-based intelligent recommendation engine that suggests outfits from a user's personal wardrobe. It combines three core logic modules — **color matching**, **occasion suitability**, and **weather-based filtering** — to produce ranked outfit suggestions without requiring any machine learning model or external AI service.

This design is intentional: rule-based AI is transparent, explainable, and appropriate for a prototype system where the goal is demonstrating intelligent logic, not training on data.

---

## 2. How the AI Works — System Overview

The recommendation process follows five sequential steps:

```
User Input (temperature, occasion, rain)
        ↓
Step 1 — Map weather category
        ↓
Step 2 — Filter wardrobe by weather + occasion
        ↓
Step 3 — Build all valid outfit combinations
        ↓
Step 4 — Score each outfit (color harmony)
        ↓
Step 5 — Attach outerwear if needed → return top 3
```

Each step is described in detail below.

---

## 3. Data Structure — ClothingItem

Every item in the wardrobe is represented as a structured data object with the following fields:

| Field | Type | Description | Example |
|---|---|---|---|
| `item_id` | String | Unique identifier | "item_1" |
| `name` | String | Human-readable name | "White Linen Shirt" |
| `category` | Enum | Type of clothing | top, bottom, dress, outerwear, shoes |
| `color` | String | Primary color | "white", "navy", "dusty rose" |
| `occasions` | List | When it can be worn | ["casual", "work"] |
| `weather_suitability` | List | Suitable weather types | ["warm", "hot"] |
| `is_clean` | Boolean | Availability status | true / false |

An **Outfit** is a composed object containing: `top`, `bottom`, `shoes`, `outerwear`, and a calculated `score`.

---

## 4. Logic Module 1 — Weather Mapping

The system converts raw temperature (°C) and rain input into a categorical weather type. This abstraction makes the filtering logic simple and readable.

| Condition | Category |
|---|---|
| Raining (any temperature) | RAINY |
| 30°C and above | HOT |
| 20°C to 29°C | WARM |
| 10°C to 19°C | COOL |
| Below 10°C | COLD |

**Why this matters:** Each clothing item stores which weather types it is suitable for. A summer dress is tagged `[HOT, WARM]` — it will never be recommended on a cold day, even if it matches the occasion.

---

## 5. Logic Module 2 — Occasion Filtering

The system supports five occasion types:

- **Casual** — everyday wear, relaxed settings
- **Work** — office-appropriate, professional but not formal
- **Formal** — events, ceremonies, high-profile settings
- **Party** — evening social events
- **Sport** — physical activity, gym, outdoor

Each clothing item carries a list of occasions it is appropriate for. The filter keeps only items that match **both** the requested occasion **and** the current weather. This two-condition filter prevents the system from suggesting a party dress for a work meeting, even if the weather matches.

```
Keep item if:
  weather IN item.weather_suitability
  AND
  occasion IN item.occasions
  AND
  item.is_clean = true
```

---

## 6. Logic Module 3 — Color Matching

Color matching is the most sophisticated part of the AI logic. Instead of comparing specific color names (which would produce too many rules), the system groups colors into **four tone families**:

| Family | Example Colors |
|---|---|
| **Neutral** | black, white, grey, beige, navy, cream |
| **Warm** | red, orange, yellow, pink, coral, burgundy |
| **Cool** | blue, green, purple, teal, mint, lavender |
| **Earth** | brown, olive, mustard, rust, tan, khaki |

Compatibility between any two items is determined by their **color groups**, not their specific colors:

| Pairing | Score | Reason |
|---|---|---|
| Neutral + Any | 1.00 | Neutrals are universally wearable |
| Neutral + Neutral | 1.00 | Classic all-neutral look |
| Earth + Earth | 0.85 | Natural tones harmonize |
| Warm + Warm | 0.80 | Analogous colors (e.g. red + coral) |
| Cool + Cool | 0.80 | Monochromatic cool tones |
| Warm + Earth | 0.75 | Autumn palette pairing |
| Cool + Earth | 0.70 | Nature-inspired contrast |
| Warm + Cool | 0.40 | Clashing complementaries |

---

## 7. Outfit Scoring Formula

Each outfit receives a score out of 100 based on color harmony across three pairings:

```
score = color_score(top, bottom)  × 50 points
      + color_score(top, shoes)   × 25 points
      + color_score(bottom, shoes)× 25 points
```

**Why these weights?** The top–bottom pairing is the most visually dominant (50 points). Shoe compatibility is split equally between both (25 + 25 points). This reflects how the human eye evaluates an outfit from head to toe.

A score of 100/100 means every pairing is perfectly compatible. Outfits are then sorted by score, and the top 3 are returned.

---

## 8. Outerwear Logic

Outerwear (coats, jackets) is handled separately from the main outfit combination step. After the top 3 outfits are selected, the system checks whether the weather requires a layer:

```
IF weather is COOL, COLD, or RAINY:
    For each of the top 3 outfits:
        Find the outerwear item with the best color match to the outfit's top
        Attach it to the outfit
```

This prevents outerwear from flooding the combination pool (which would create hundreds of near-identical outfits) while still ensuring it is included when weather demands it.

---

## 9. AI Chat — Vouge Stylist

Beyond the recommendation engine, the system includes an AI chat assistant called **Vouge**. It adapts its personality to the user's selected style aesthetic:

| Style | Chat Personality |
|---|---|
| Kawaii | Bubbly, enthusiastic, uses 🎀 |
| Emo | Poetic, dramatic, darkly witty 🖤 |
| Minimalist | Precise, calm, no unnecessary words |
| Streetwear | Casual, cool, hype language 🔥 |
| Cottagecore | Gentle, dreamy, nature references 🌿 |
| Y2K | Nostalgic, excitable, "bestie" energy ✨ |
| Gyaru | Glamorous, confident, encouraging 💅 |
| Formal | Professional, authoritative |

The chat handles queries including: outfit suggestions from the wardrobe, shopping recommendations (with direct search links to Google, ASOS, Pinterest, Depop), color palette advice, brand recommendations, and style tips.

When an Anthropic API key is provided, the chat upgrades to full Claude AI (claude-haiku-4-5). Without it, a rule-based response system handles queries using intent detection across categories: greetings, outfit requests, shopping queries, color questions, brand questions, and style tips.

---

## 10. Why Rule-Based AI?

| Approach | Rule-Based (ours) | Machine Learning |
|---|---|---|
| Requires training data | No | Yes (thousands of images) |
| Explainable decisions | Yes | Often not |
| Works offline | Yes | Depends |
| Appropriate for prototype | ✓ Perfect fit | Overkill |
| Easy to adjust rules | Yes | Requires retraining |

For a prototype demonstrating design and logic, rule-based AI is the correct choice. It produces explainable, predictable results and can be extended with new rules without any model retraining.

---

## 11. Summary of AI Features

| Feature | Description |
|---|---|
| Weather-based filtering | Maps temperature to categories; filters wardrobe accordingly |
| Occasion matching | 5 occasion types; dual-condition filter ensures correctness |
| Color grouping | 4 tone families; 8 compatibility rules |
| Outfit scoring | Weighted formula (100-point scale) |
| Outerwear logic | Attached post-ranking for cold/rainy weather |
| AI chat | Style-adaptive personality; handles outfit, shopping, tips queries |
| Shopping integration | Direct search links to Google, ASOS, Pinterest, Depop |
| Style profiles | 8 aesthetics (Kawaii, Gyaru, Emo, Minimalist, Formal, Streetwear, Cottagecore, Y2K) |
