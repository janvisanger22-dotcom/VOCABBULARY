# vougeabulary — Presentation Slides Content
### All Sections — Ready to Copy into PowerPoint / Google Slides

---

## SLIDE 1 — TITLE SLIDE

**Main Title:** vougeabulary
**Subtitle:** An AI-Powered Smart Wardrobe & Outfit Recommendation System
**Team:** Janvi · Raman · Harman · Tanish · Samaira
**Course / Subject:** [Your course name]
**Date:** [Presentation date]

*Design tip: Dark background, gradient gold/pink title text, minimalist layout*

---

## SLIDE 2 — TEAM ROLES

**Title:** Meet the Team

| Name | Role |
|---|---|
| Janvi | Research & Concept Lead |
| Raman | Design & Frontend Lead |
| Harman | Backend Lead — Core API |
| Tanish | Backend Lead — Database |
| Samaira | AI & Recommendation Lead |

---

---
# SECTION 1: RESEARCH & CONCEPT — Janvi
---

## SLIDE 3 — INTRODUCTION

**Title:** What is vougeabulary?

**Bullet Points:**
- A blend of *vogue* + *vocabulary* — a language of personal style
- AI-powered digital wardrobe management system
- Suggests intelligent outfits based on **weather**, **occasion**, and **personal style**
- Prototype demonstrating AI concepts applied to everyday fashion decisions
- Target users: young adults aged 16–30 who struggle with daily outfit decisions

**Talking point:** "vougeabulary is not just an app — it's a smart wardrobe assistant that turns the clothes you already own into a curated, intelligent system."

---

## SLIDE 4 — PROBLEM STATEMENT (Part 1)

**Title:** The Problem — "I Have Nothing to Wear"

**Main points:**
- 82% of people own more clothes than they think they do
- Most people wear only 20% of their wardrobe regularly
- Result: wasted money, overcrowded closets, sustainable fashion concerns

**Visual suggestion:** Two-column image — overflowing wardrobe on left, frustrated person on right

---

## SLIDE 5 — PROBLEM STATEMENT (Part 2)

**Title:** Three Core Pain Points

**Pain Point 1 — Poor Wardrobe Visibility**
> Users forget what they own → they buy more → wardrobe grows but feels empty

**Pain Point 2 — Decision Fatigue**
> Choosing an outfit for the right weather, occasion, and color match requires time and knowledge most people don't have

**Pain Point 3 — Unsustainable Habits**
> Fashion industry = 10% of global CO₂ emissions. Maximizing existing wardrobe use reduces this significantly.

---

## SLIDE 6 — OUR SOLUTION

**Title:** How vougeabulary Solves This

| Problem | Our Solution |
|---|---|
| Can't see full wardrobe | Digital wardrobe — every item catalogued |
| No outfit guidance | AI engine: weather + occasion + color rules |
| Bad color matching | Rule-based color compatibility system |
| Impulse buying | Smart shopping gaps analysis |
| No style identity | 8 aesthetic style profiles |

---

## SLIDE 7 — KEY FEATURES

**Title:** 5 Core Features

1. **Style Profile Selection** — 8 aesthetics: Kawaii, Gyaru, Emo, Minimalist, Formal, Streetwear, Cottagecore, Y2K
2. **Digital Wardrobe** — Add, view, and manage every clothing item you own
3. **AI Outfit Recommendations** — Weather + occasion + color-based ranking
4. **AI Stylist Chat (Vouge)** — Conversational fashion advice with adaptive personality
5. **Shopping Discovery** — Style-curated links to Google, ASOS, Pinterest, Depop

---

---
# SECTION 2: DESIGN & FRONTEND — Raman
---

## SLIDE 8 — DESIGN PHILOSOPHY

**Title:** Design Approach — Dark Luxury Fashion

**Principles:**
- **Dark-first aesthetic** — reflects fashion editorial design culture
- **Dynamic accent system** — app color changes when style is selected (personalised feel)
- **Minimal friction** — everything accessible in one click
- **Card-based layout** — visual, scannable, fashion-forward

**Color System:**
- Background: `#0A0A0A` (near black)
- Cards: `#1C1C1C`
- Text: `#F0F0F0`
- Accent: *changes per style*

---

## SLIDE 9 — SCREEN: STYLE TAB

**Title:** Screen 1 — Style Selection + Outfits

**Describe on slide:**
- 8 style cards in a 2×4 grid — click to select aesthetic
- Clicking a style INSTANTLY changes app accent color to match
- Temperature slider (−10°C to 45°C) with live weather badge
- Occasion pill buttons (Casual / Work / Formal / Party / Sport)
- Rain toggle switch
- "Get Outfits →" button generates ranked outfit cards

*Include a screenshot of the actual app running*

---

## SLIDE 10 — SCREEN: WARDROBE TAB

**Title:** Screen 2 — Digital Wardrobe

**Two-column layout:**
- **Left:** Add Item form (name, category, color, occasions, weather tags)
- **Right:** Wardrobe grid — each card shows color swatch, item name, category badge

**Features:**
- Color circles match the actual item color
- Hover to reveal delete button
- Item count shown live

*Include a screenshot of the wardrobe tab with items loaded*

---

## SLIDE 11 — SCREEN: AI CHAT + SHOP

**Title:** Screens 3 & 4 — AI Stylist + Shopping

**Chat Screen:**
- AI messages: left-aligned dark bubble with ✦ avatar
- User messages: right-aligned gradient bubble
- Personality adapts to selected style (e.g. Kawaii = bubbly 🎀, Emo = dark 🖤)
- Chat includes clickable shopping links

**Shop Screen:**
- Style header card with emoji, palette, description
- Brand recommendations list
- Search buttons: Google · ASOS · Pinterest · Depop

---

---
# SECTION 3: BACKEND CORE API — Harman
---

## SLIDE 12 — SYSTEM ARCHITECTURE

**Title:** System Architecture

```
[User Browser]
      ↕  HTTP / JSON
[Flask Server — Python]
    ↙            ↘
[AI Engine]   [Data Layer]
(recommendation) (wardrobe.json)
```

**Technology stack:**
- Language: Python 3
- Web framework: Flask
- AI Chat: Anthropic Claude API (optional) / Rule-based fallback
- Data: JSON flat file (prototype) → MongoDB in production
- Frontend: HTML5 + CSS3 + Vanilla JavaScript

---

## SLIDE 13 — SYSTEM FLOW

**Title:** How a Recommendation Request Works

1. User sets temperature, occasion, rain toggle
2. Clicks "Get Outfits →"
3. Browser sends `POST /api/recommend` with `{ temp, occasion, rain }`
4. Flask loads wardrobe from disk
5. AI engine filters items by weather + occasion
6. Engine scores all combinations using color rules
7. Returns top 3 ranked outfits as JSON
8. Browser renders outfit cards with color swatches

*Total time: < 100 milliseconds*

---

## SLIDE 14 — API ENDPOINTS

**Title:** API Design — 6 Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the app |
| GET | `/api/wardrobe` | Get all wardrobe items |
| POST | `/api/wardrobe` | Add a new item |
| DELETE | `/api/wardrobe/<id>` | Remove an item |
| POST | `/api/recommend` | Get outfit recommendations |
| POST | `/api/chat` | AI stylist conversation |
| GET | `/api/shop/<style>` | Shopping info for a style |

---

## SLIDE 15 — REQUEST / RESPONSE EXAMPLE

**Title:** API in Action — Sample Request & Response

**Request:**
```json
POST /api/recommend
{
  "temp": 15,
  "occasion": "work",
  "rain": false
}
```

**Response:**
```json
{
  "outfits": [{
    "score": 100,
    "items": [
      { "role": "Top",    "name": "Black Turtleneck", "color": "black" },
      { "role": "Bottom", "name": "Black Trousers",   "color": "black" },
      { "role": "Shoes",  "name": "Black Heels",      "color": "black" }
    ]
  }]
}
```

---

---
# SECTION 4: DATABASE & INTEGRATION — Tanish
---

## SLIDE 16 — DATA STORAGE

**Title:** Data Architecture

**Storage approach:** JSON flat-file (prototype)
- File: `data/wardrobe.json`
- No database server required — ideal for prototype
- Human-readable, easy to inspect
- Easily upgradable to MongoDB or PostgreSQL in production

**Why JSON for prototype:**
- Zero setup — works out of the box
- Readable format for review and demonstration
- All CRUD operations (Create, Read, Update, Delete) supported

---

## SLIDE 17 — DATA SCHEMA

**Title:** ClothingItem Data Schema

```json
{
  "id":        "item_1_white_linen_shirt",
  "name":      "White Linen Shirt",
  "category":  "top",
  "color":     "white",
  "occasions": ["casual", "work"],
  "weather":   ["hot", "warm"],
  "is_clean":  true
}
```

**6 categories:** top · bottom · dress · outerwear · shoes · accessory
**5 occasions:** casual · work · formal · party · sport
**5 weather types:** hot · warm · cool · cold · rainy

---

## SLIDE 18 — DATA FLOW DIAGRAM

**Title:** How Data Connects to the System

```
wardrobe.json (disk)
        ↓  load_wardrobe()
   Python dict list
        ↓  wardrobe_to_engine()
  ClothingItem objects
        ↓  RecommendationEngine
   Outfit objects (scored)
        ↓  JSON serialization
  HTTP response → Browser
```

**Key integration point:** `wardrobe_to_engine()` converts raw JSON into typed Python objects that the AI engine can process.

---

## SLIDE 19 — FUTURE DATABASE DESIGN

**Title:** Production Database Design (MongoDB)

```
Collection: users
  → _id, email, name, selected_style

Collection: clothing_items
  → _id, user_id, name, category,
     color, occasions[], weather[]

Collection: outfit_history
  → _id, user_id, items[], score,
     worn_on, occasion, weather
```

**Upgrade path:** Replace `load_wardrobe()` / `save_wardrobe()` with MongoDB queries — no other code changes needed.

---

---
# SECTION 5: AI & RECOMMENDATION — Samaira
---

## SLIDE 20 — AI APPROACH

**Title:** Why Rule-Based AI?

| | Rule-Based (ours) | Machine Learning |
|---|---|---|
| Training data needed | ❌ No | ✅ Yes (thousands of images) |
| Explainable decisions | ✅ Yes | ❌ Often not |
| Works offline | ✅ Yes | Depends |
| Right for prototype | ✅ Perfect | ❌ Overkill |
| Adjustable without retraining | ✅ Yes | ❌ No |

**Conclusion:** Rule-based AI produces transparent, explainable, predictable results — exactly what a prototype needs.

---

## SLIDE 21 — COLOR MATCHING SYSTEM

**Title:** Color Matching — The Core Logic

**4 Tone Families:**
- **Neutral:** black, white, grey, beige, navy → matches everything (score: 1.00)
- **Warm:** red, orange, yellow, pink, coral
- **Cool:** blue, green, purple, teal, mint
- **Earth:** brown, olive, mustard, rust, tan

**Key Rule:** Neutrals are universally compatible. Warm + Cool = clash (0.40). Same family = good match (0.80+).

---

## SLIDE 22 — OUTFIT SCORING FORMULA

**Title:** How Outfits Are Scored (0–100)

```
score = color_score(top, bottom)   × 50 pts
      + color_score(top, shoes)    × 25 pts
      + color_score(bottom, shoes) × 25 pts
```

**Example — Black Turtleneck + Black Trousers + Black Heels:**
- Black + Black = neutral + neutral = 1.00 × 50 = 50 pts
- Black + Black = 1.00 × 25 = 25 pts
- Black + Black = 1.00 × 25 = 25 pts
- **Total: 100/100 ✓**

---

## SLIDE 23 — RECOMMENDATION ALGORITHM

**Title:** The 5-Step Recommendation Process

1. **Map weather** — temperature → HOT / WARM / COOL / COLD / RAINY
2. **Filter wardrobe** — keep only items matching weather AND occasion
3. **Build combinations** — every top × bottom pair, every dress option
4. **Score outfits** — apply color formula to each combination
5. **Attach outerwear** — add coat/jacket to top 3 if weather is cool/cold/rainy

---

## SLIDE 24 — AI STYLIST CHAT

**Title:** Vouge — The AI Stylist

**Handles 6 query types:**
- "What should I wear?" → wardrobe-based outfit suggestion
- "Where should I shop?" → brand + search link recommendations
- "What colors work for my style?" → style palette explanation
- "What brands match my style?" → curated brand list
- "Give me style tips" → aesthetic-specific fashion advice
- General questions → personality-matched responses

**8 personality modes** — one per style (Kawaii = bubbly 🎀, Emo = dramatic 🖤, etc.)

---

## SLIDE 25 — STYLE PROFILES

**Title:** 8 Fashion Aesthetics

| Style | Tagline | Accent Color |
|---|---|---|
| 🎀 Kawaii | Sweet & Dreamy | Pastel Pink |
| 💅 Gyaru | Glam & Fierce | Hot Pink |
| 🖤 Emo | Dark & Expressive | Purple |
| ◻ Minimalist | Clean & Elevated | Warm Beige |
| 🎩 Formal | Sharp & Sophisticated | Steel Blue |
| 🧢 Streetwear | Urban & Bold | Bold Red |
| 🌿 Cottagecore | Romantic & Natural | Sage Green |
| ✨ Y2K | Retro Futuristic | Plum |

---

---
# CLOSING SLIDES
---

## SLIDE 26 — LIVE DEMO

**Title:** System Demo

*[Run the actual app during presentation]*

Demo script:
1. Open `http://localhost:5000`
2. Select **Kawaii** style — show accent color change
3. Set temperature to 28°C, occasion to Party, no rain
4. Click "Get Outfits" — show ranked results
5. Go to Wardrobe — add a new item live
6. Go to AI Stylist — type "what should I wear tomorrow?" — show chat
7. Go to Shop — show brand + search links

---

## SLIDE 27 — CONCLUSION

**Title:** What We Demonstrated

✅ A complete AI-powered system design from concept to working prototype
✅ Rule-based AI logic: color matching, occasion filtering, weather mapping
✅ Full system architecture: frontend, backend API, database, AI engine
✅ Conversational AI with adaptive personality
✅ A real-world problem solved with clear, structured technology

**Future possibilities:** image recognition for auto-cataloguing, real ML for color trend prediction, mobile app, social sharing of outfits

---

## SLIDE 28 — THANK YOU

**Title:** Thank You

*vougeabulary — Dress smarter, not harder.*

**Questions?**

Team: Janvi · Raman · Harman · Tanish · Samaira
