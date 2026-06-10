# vougeabulary — Full Project Report
### An AI-Based Smart Wardrobe & Outfit Recommendation System

---
**Team Members**

| Role | Name |
|---|---|
| Research & Concept Lead | Janvi |
| Design & Frontend Lead | Raman |
| Backend Lead — Core API | Harman |
| Backend Lead — Database & Integration | Tanish |
| AI & Recommendation Lead | Samaira |

---

# PART 1 — RESEARCH & CONCEPT
*Lead: Janvi*

---

## 1.1 Introduction

In today's fast-paced world, fashion plays a significant role in how people present themselves and feel about their daily lives. Yet despite owning full wardrobes, most people find themselves standing in front of their closet every morning with one recurring thought: *"I have nothing to wear."*

**vougeabulary** (a blend of *vogue* and *vocabulary*) is an AI-powered smart wardrobe assistant designed to solve this everyday problem. The system allows users to digitally catalogue the clothes they already own and receive intelligent, context-aware outfit recommendations based on factors such as the current weather, the occasion they are dressing for, and their personal style preferences.

This project is developed as a prototype — a conceptual demonstration of how artificial intelligence can be practically applied to fashion and everyday decision-making. The goal is not to build a fully deployed application, but to demonstrate a well-structured system design, clear logic, and effective use of AI concepts in a real-world scenario.

---

## 1.2 Problem Statement

### The Core Problem

Millions of people face two contradictory realities every day:

1. **They feel like they have nothing to wear** — even when their wardrobe is full.
2. **They buy more clothes than they need** — because they cannot track or visualize what they already own.

These two problems are directly connected. When users cannot see or remember their full wardrobe, they under-utilize existing items and make unnecessary purchases — leading to wasted money, overcrowded wardrobes, and increased fashion waste.

### Secondary Problems

Beyond the core issue, users also struggle with:

- **Decision fatigue** — Choosing an outfit every morning consumes mental energy, especially when trying to consider weather, occasion, and personal style simultaneously.
- **Poor color coordination** — Most people are not trained in color theory and struggle to know which colors work well together.
- **Occasion mismatches** — Without a system, people may arrive at events over- or under-dressed because they lacked guidance when getting ready.
- **Unsustainable fashion habits** — The fashion industry is one of the world's largest polluters. Systems that reduce unnecessary purchasing have meaningful environmental benefits.

### How vougeabulary Addresses These Problems

| Problem | vougeabulary Solution |
|---|---|
| Cannot visualize wardrobe | Digital wardrobe — every item catalogued with photo, color, category |
| No outfit guidance | AI recommendation engine based on weather + occasion + color rules |
| Poor color matching | Rule-based color compatibility system using tone group theory |
| Impulse buying | Smart shopping suggestions based on *gaps* in the wardrobe |
| Style identity unclear | Style profile system (8 aesthetics) to anchor personal preferences |

---

## 1.3 Project Concept & Features

### What is vougeabulary?

vougeabulary is a digital wardrobe management and AI outfit recommendation system. Users interact with it through a web-based interface with four core modules:

**Module 1 — Style Profile Selection**
Users select their fashion aesthetic from eight defined styles: Kawaii, Gyaru, Emo, Minimalist, Formal, Streetwear, Cottagecore, and Y2K. This profile shapes recommendations, AI chat personality, and shopping suggestions throughout the entire app.

**Module 2 — Digital Wardrobe**
Users add every clothing item they own into the system, recording the item name, category (top, bottom, dress, outerwear, shoes), color, occasions it is suitable for, and weather conditions it is appropriate in. The wardrobe becomes a persistent, searchable database of their actual clothes.

**Module 3 — AI Outfit Recommendations**
Users input today's temperature, their occasion, and whether it is raining. The AI engine filters the wardrobe, scores all possible outfit combinations using color harmony rules, and returns the top 3 ranked outfits — complete with outerwear suggestions for cold or rainy weather.

**Module 4 — AI Stylist Chat (Vouge)**
An AI chat assistant named Vouge answers questions about outfits, style, shopping, color palettes, and brand recommendations. The assistant's personality adapts to the user's selected style aesthetic.

**Module 5 — Shopping Discovery**
Based on the user's style profile, the system curates brand recommendations and generates direct search links to shopping platforms (Google Shopping, ASOS, Pinterest, Depop) for style-relevant items.

### Target Users

- Young adults aged 16–30 who are fashion-conscious but time-constrained
- Students and working professionals who dress for multiple different contexts
- Sustainability-minded individuals who want to maximize their existing wardrobe before buying new items

### Project Scope (Prototype)

As this is a prototype, the focus is on:
- System design clarity and logical correctness
- Demonstrating AI concepts through rule-based intelligence
- Building a working interface that showcases the full user journey

It does not include: user authentication, cloud hosting, image recognition, or a native mobile app. These would be features of a production version.

---

# PART 2 — DESIGN & FRONTEND
*Lead: Raman*

---

## 2.1 Design Philosophy

The UI of vougeabulary follows a **dark luxury fashion aesthetic** — reflecting the world of fashion editorials, high-end app design, and modern style culture. The design principles are:

1. **Dark-first** — Deep backgrounds (#0A0A0A) with light text create a sophisticated, editorial feel
2. **Dynamic accent system** — The app's accent color changes when the user selects a style profile, making the experience feel personalized
3. **Minimal friction** — No unnecessary clicks; every input is on-screen and immediately accessible
4. **Card-based layout** — Clothing items and outfits are presented as visual cards with color swatches, making them easy to scan

### Color System

| Element | Color Value | Usage |
|---|---|---|
| Background | `#0A0A0A` | Page background |
| Surface | `#141414` | Input backgrounds |
| Card | `#1C1C1C` | All cards and panels |
| Border | `#2A2A2A` | Dividers and card edges |
| Text | `#F0F0F0` | Primary text |
| Muted text | `#888888` | Labels, secondary info |
| Accent | Dynamic | Changes per style profile |

Each style has its own accent color: Kawaii (#FFB7C5 pastel pink), Gyaru (#FF69B4 hot pink), Emo (#9B59B6 purple), Minimalist (#C8B89A warm beige), Formal (#4A90D9 steel blue), Streetwear (#E74C3C bold red), Cottagecore (#87A878 sage green), Y2K (#DDA0DD plum).

---

## 2.2 Screen Descriptions

### Screen 1 — Header / Navigation Bar (Persistent)

The navigation bar appears at the top of every screen. It contains:
- The **vougeabulary logo** in a gradient (accent to gold)
- **Four navigation tabs**: ✦ Style | 👗 Wardrobe | 💬 AI Stylist | 🛍️ Shop
- A **style pill** in the top right showing the currently selected style emoji and name

The bar uses blur/frosted glass effect so page content scrolls underneath it without visual clutter.

---

### Screen 2 — Style Tab (Home)

**Purpose:** Style selection + outfit recommendations

**Layout (top to bottom):**

1. **Section title:** "Choose Your Aesthetic"
2. **Style Grid (2×4):** Eight clickable cards, one per style. Each card shows the style emoji, name, and tagline. Clicking a card instantly changes the app's accent color and updates the header pill. The selected card gets a glowing border in the accent color.

3. **Controls Bar:** A single-row panel containing:
   - Temperature slider (−10°C to 45°C) with live °C label and a colored weather badge (HOT/WARM/COOL/COLD/RAINY)
   - Occasion pills (Casual, Work, Formal, Party, Sport) — toggle selection
   - Rain toggle switch
   - "Get Outfits →" button (gradient background)

4. **Outfit Results:** After clicking "Get Outfits", up to three outfit cards appear side by side. Each card shows:
   - Rank (#1, #2, #3)
   - A color-coded match score bar (e.g. 87/100)
   - Each clothing item with a colored dot (matching the item's actual color), role label, and item name

---

### Screen 3 — Wardrobe Tab

**Purpose:** Manage the user's digital wardrobe

**Layout (two-column):**

**Left column — Add Item Form:**
- Text input: Item name
- Dropdown: Category (top / bottom / dress / outerwear / shoes / accessory)
- Text input: Color
- Checkbox pills: Occasions (multi-select)
- Checkbox pills: Weather (multi-select)
- "Add to Wardrobe" button

**Right column — Wardrobe Grid:**
- Item count at the top ("17 items")
- Grid of cards, one per clothing item. Each card shows:
  - A colored circle swatch matching the item's color
  - Item name (bold)
  - Category badge
  - Occasion tags
  - A delete button (appears on hover, red circle in top-right corner)

---

### Screen 4 — AI Stylist Tab (Chat)

**Purpose:** Conversational AI for fashion guidance

**Layout:**
- Chat history area (scrollable, fills most of the screen)
  - AI messages: left-aligned, dark card bubble with a ✦ avatar
  - User messages: right-aligned, gradient bubble
- "Powered by" label (shows "Vouge AI" or "Claude AI" depending on API key)
- Input row at the bottom: text field + send button

The chat opens with a personality-specific greeting that matches the current style (e.g. "Kyaaa~ hiii!! 🎀" for Kawaii, "...hey. 🖤" for Emo).

---

### Screen 5 — Shop Tab

**Purpose:** Shopping discovery by style

**Layout (top to bottom):**

1. **Style Header Card:** Large card showing the style emoji, name, tagline, description, and a row of color palette dots with color names.

2. **Two-column grid:**
   - Left: **Recommended Brands** — a list of brands known for this aesthetic, each with a colored accent dot
   - Right: **Search & Buy** — for each search term, four platform buttons (Google / ASOS / Pinterest / Depop) that open in a new tab

---

## 2.3 UI Principles Applied

- **Affordance:** Every interactive element looks clickable — buttons have hover states, cards lift on hover, sliders have visible thumb handles
- **Feedback:** Selecting a style immediately changes the color scheme; submitting the form immediately renders results
- **Consistency:** The same card design language, spacing, and color variables are used throughout every screen
- **Accessibility:** Sufficient contrast between text and background; font sizes never below 9px; interactive targets are minimum 44×44px

---

# PART 3 — BACKEND LEAD (CORE API)
*Lead: Harman*

---

## 3.1 System Architecture Overview

vougeabulary uses a client-server architecture where:
- The **frontend** (HTML/CSS/JavaScript) runs in the user's browser
- The **backend** (Python/Flask) handles all business logic and data operations
- The **AI module** (Python) is called by the backend to generate recommendations

```
[Browser / User Interface]
         ↕  HTTP requests (JSON)
[Flask Backend — app.py]
    ↕              ↕
[AI Engine]   [Data Layer — wardrobe.json]
```

---

## 3.2 System Flow

The complete user journey through the system:

```
1. User opens the app in browser
         ↓
2. Browser sends GET request to Flask server
         ↓
3. Flask serves the HTML page
         ↓
4. User selects style, sets temperature/occasion, clicks "Get Outfits"
         ↓
5. Browser sends POST /api/recommend with { temp, occasion, rain }
         ↓
6. Backend loads wardrobe from wardrobe.json
         ↓
7. Backend calls RecommendationEngine with wardrobe + user inputs
         ↓
8. AI engine filters, scores, and ranks outfit combinations
         ↓
9. Backend returns ranked outfits as JSON
         ↓
10. Browser renders outfit cards in the UI
```

---

## 3.3 API Endpoints

The backend exposes the following REST API endpoints:

---

### GET `/`
**Purpose:** Serve the main application page
**Response:** HTML page (index.html rendered by Flask)

---

### GET `/api/wardrobe`
**Purpose:** Retrieve all clothing items in the user's wardrobe
**Response:**
```json
[
  {
    "id": "item_1_white_linen_shirt",
    "name": "White Linen Shirt",
    "category": "top",
    "color": "white",
    "occasions": ["casual", "work"],
    "weather": ["hot", "warm"],
    "is_clean": true
  }
]
```

---

### POST `/api/wardrobe`
**Purpose:** Add a new clothing item to the wardrobe
**Request Body:**
```json
{
  "name": "Navy Blazer",
  "category": "outerwear",
  "color": "navy",
  "occasions": ["formal", "work"],
  "weather": ["cool", "cold"]
}
```
**Response:**
```json
{ "success": true, "item": { ... full item with generated id ... } }
```

---

### DELETE `/api/wardrobe/<item_id>`
**Purpose:** Remove a clothing item from the wardrobe
**URL Parameter:** `item_id` — the unique ID of the item to delete
**Response:**
```json
{ "success": true }
```

---

### POST `/api/recommend`
**Purpose:** Generate outfit recommendations based on weather and occasion
**Request Body:**
```json
{
  "temp": 22,
  "occasion": "casual",
  "rain": false
}
```
**Response:**
```json
{
  "outfits": [
    {
      "score": 100.0,
      "items": [
        { "role": "Top/Dress", "name": "White Linen Shirt", "color": "white", "hex": "#FFFFFF" },
        { "role": "Bottom",    "name": "Beige Chinos",      "color": "beige", "hex": "#C8B89A" },
        { "role": "Shoes",     "name": "Brown Loafers",     "color": "brown", "hex": "#6D4C41" }
      ]
    }
  ]
}
```

---

### POST `/api/chat`
**Purpose:** Send a message to the AI stylist and receive a response
**Request Body:**
```json
{
  "message": "What should I wear today?",
  "style": "minimalist",
  "history": [
    { "role": "user",      "content": "Hi!" },
    { "role": "assistant", "content": "Hello! How can I help?" }
  ]
}
```
**Response:**
```json
{
  "response": "From your wardrobe, try the **White Linen Shirt** paired with **Beige Chinos**...",
  "powered_by": "Vouge AI"
}
```

---

### GET `/api/shop/<style>`
**Purpose:** Get shopping information for a given style
**URL Parameter:** `style` — one of: kawaii, gyaru, emo, minimalist, formal, streetwear, cottagecore, y2k
**Response:**
```json
{
  "name": "Minimalist",
  "tagline": "Clean & Elevated",
  "colors": ["white", "black", "grey", "beige"],
  "brands": ["COS", "Everlane", "Uniqlo"],
  "links": [
    {
      "term": "minimalist capsule wardrobe",
      "google":    "https://www.google.com/search?q=minimalist+capsule+wardrobe",
      "asos":      "https://www.asos.com/search/?q=minimalist+capsule+wardrobe",
      "pinterest": "https://www.pinterest.com/search/pins/?q=minimalist+capsule+wardrobe",
      "depop":     "https://www.depop.com/search/?q=minimalist+capsule+wardrobe"
    }
  ]
}
```

---

## 3.4 Error Handling

| Scenario | Backend Behaviour |
|---|---|
| Wardrobe is empty when requesting recommendations | Returns `{ "outfits": [], "empty": true }` |
| Invalid occasion or category value | Item silently skipped; no crash |
| No API key for AI chat | Falls back to rule-based response system |
| Item ID not found on delete | Returns success (idempotent delete) |

---

# PART 4 — BACKEND (DATABASE & INTEGRATION)
*Lead: Tanish*

---

## 4.1 Data Storage Overview

vougeabulary uses a **JSON-based flat-file storage** system. All wardrobe data is stored in a single file: `data/wardrobe.json`. This approach is appropriate for a prototype because:

- No database server setup is required
- Data is human-readable and easy to inspect
- The file is loaded into memory on each request (fast for small datasets)
- It can be replaced with a real database (MongoDB, PostgreSQL) in production with minimal changes to the backend code

---

## 4.2 Data Schema — Clothing Item

Every clothing item in the system is stored as a JSON object with the following schema:

```json
{
  "id":        "string  — unique identifier (auto-generated)",
  "name":      "string  — display name of the item",
  "category":  "string  — one of: top, bottom, dress, outerwear, shoes, accessory",
  "color":     "string  — primary color in lowercase (e.g. 'white', 'navy', 'dusty rose')",
  "occasions": "array   — list of: casual, work, formal, party, sport",
  "weather":   "array   — list of: hot, warm, cool, cold, rainy",
  "is_clean":  "boolean — whether the item is available to wear (default: true)"
}
```

**ID Generation Rule:**
IDs are generated deterministically from the item count and name:
```
id = "item_" + (total_items + 1) + "_" + name.lowercase().replace_spaces("_")
Example: "item_5_blue_jeans"
```

---

## 4.3 Sample Wardrobe Data

```json
[
  {
    "id": "item_1_white_linen_shirt",
    "name": "White Linen Shirt",
    "category": "top",
    "color": "white",
    "occasions": ["casual", "work"],
    "weather": ["hot", "warm"],
    "is_clean": true
  },
  {
    "id": "item_8_red_floral_dress",
    "name": "Red Floral Dress",
    "category": "dress",
    "color": "red",
    "occasions": ["party", "casual"],
    "weather": ["hot", "warm"],
    "is_clean": true
  }
]
```

---

## 4.4 Data Relationships

Although the data is flat (no foreign keys), there are logical relationships between entities:

```
Wardrobe (1)
    └── ClothingItem (many)
            ├── category → maps to Category enum
            ├── occasions → maps to Occasion enum list
            └── weather → maps to Weather enum list

RecommendationRequest (1)
    ├── temp      → maps to Weather category
    ├── occasion  → must exist in Occasion enum
    └── rain      → overrides temp-based Weather

Outfit (output)
    ├── top       → reference to ClothingItem
    ├── bottom    → reference to ClothingItem
    ├── outerwear → reference to ClothingItem (nullable)
    └── shoes     → reference to ClothingItem (nullable)
```

---

## 4.5 Data Validation Rules

Before saving a new item, the backend enforces:

| Field | Validation |
|---|---|
| `name` | Must be non-empty string |
| `category` | Must be one of the 6 valid category values |
| `color` | Must be non-empty string (any color name accepted) |
| `occasions` | Must contain at least one valid occasion |
| `weather` | Must contain at least one valid weather type |

Items that fail validation during the recommendation phase (e.g. malformed data from a previous version) are silently skipped rather than crashing the system.

---

## 4.6 How Data Connects to the Backend

The data flow between storage and the AI recommendation engine:

```
wardrobe.json (disk)
      ↓  load_wardrobe()
Python list of dictionaries
      ↓  wardrobe_to_engine()
Wardrobe object containing ClothingItem objects
      ↓  RecommendationEngine.recommend()
List of Outfit objects (scored and ranked)
      ↓  JSON serialization
HTTP response to browser
```

The `wardrobe_to_engine()` function is the integration point between the database layer (raw JSON) and the AI layer (typed Python objects). It converts each dictionary into a `ClothingItem` object with proper enum types, enabling the recommendation engine to work with structured data.

---

## 4.7 Future Database Design (Production)

For a production version, the flat-file storage would be replaced with a relational or document database. A MongoDB schema would look like:

**Collection: `users`**
```
{ _id, email, name, selected_style, created_at }
```

**Collection: `clothing_items`**
```
{ _id, user_id (ref: users), name, category, color, occasions[], weather[], is_clean, created_at }
```

**Collection: `outfit_history`**
```
{ _id, user_id (ref: users), items[] (ref: clothing_items), score, worn_on, occasion, weather }
```

---

# PART 5 — AI & RECOMMENDATION SYSTEM
*Lead: Samaira*

---

## 5.1 Overview

The AI component of vougeabulary is a rule-based intelligent recommendation engine that suggests outfits from a user's personal wardrobe. It combines three core logic modules — **color matching**, **occasion suitability**, and **weather-based filtering** — to produce ranked outfit suggestions without requiring any machine learning model.

This design is intentional: rule-based AI is transparent, explainable, and appropriate for a prototype where the goal is demonstrating intelligent logic rather than training on data.

---

## 5.2 Recommendation Algorithm — Step by Step

```
User Input: temperature (°C), occasion, raining (yes/no)
        ↓
Step 1 — Map weather category
        ↓
Step 2 — Filter wardrobe by weather + occasion
        ↓
Step 3 — Build all valid outfit combinations
        ↓
Step 4 — Score each outfit on 0–100 scale
        ↓
Step 5 — Attach outerwear if cold/rainy → return top 3
```

---

## 5.3 Weather Mapping Logic

| Condition | Category |
|---|---|
| Raining (any temperature) | RAINY |
| 30°C and above | HOT |
| 20–29°C | WARM |
| 10–19°C | COOL |
| Below 10°C | COLD |

---

## 5.4 Color Matching System

Colors are grouped into four tone families:

| Family | Colors |
|---|---|
| Neutral | black, white, grey, beige, navy, cream |
| Warm | red, orange, yellow, pink, coral, burgundy |
| Cool | blue, green, purple, teal, mint, lavender |
| Earth | brown, olive, mustard, rust, tan, khaki |

Compatibility scoring:

| Pairing | Score |
|---|---|
| Neutral + Any | 1.00 |
| Earth + Earth | 0.85 |
| Warm + Warm | 0.80 |
| Cool + Cool | 0.80 |
| Warm + Earth | 0.75 |
| Cool + Earth | 0.70 |
| Warm + Cool | 0.40 |

**Outfit score formula:**
```
score = color_score(top, bottom) × 50
      + color_score(top, shoes)  × 25
      + color_score(bottom, shoes) × 25
```

---

## 5.5 AI Stylist Chat — Vouge

The system includes a style-adaptive AI chat assistant. Its personality changes based on the user's selected aesthetic:

| Style | Personality |
|---|---|
| Kawaii | Bubbly, enthusiastic 🎀 |
| Emo | Poetic, darkly expressive 🖤 |
| Minimalist | Precise, calm, no fluff |
| Streetwear | Cool, casual, hype language 🔥 |
| Cottagecore | Gentle, dreamy 🌿 |
| Y2K | Nostalgic, bestie energy ✨ |
| Gyaru | Glamorous, confident 💅 |
| Formal | Professional, authoritative |

The chat handles: outfit suggestions, shopping recommendations with direct links, color palette advice, brand recommendations, and style tips.

---

## 5.6 Style Profiles

The system defines 8 fashion aesthetics, each with its own color palette, keywords, brand recommendations, and search terms:

| Style | Tagline | Core Colors | Sample Brands |
|---|---|---|---|
| Kawaii | Sweet & Dreamy | Pink, White, Lavender | Angelic Pretty, Swimmer |
| Gyaru | Glam & Fierce | Coral, Gold, Hot Pink | MOUSSY, Liz Lisa |
| Emo | Dark & Expressive | Black, Dark Red, Purple | Killstar, Disturbia |
| Minimalist | Clean & Elevated | White, Black, Beige | COS, Everlane, Uniqlo |
| Formal | Sharp & Sophisticated | Navy, Black, Charcoal | Hugo Boss, Massimo Dutti |
| Streetwear | Urban & Bold | Black, White, Red | Supreme, Stussy |
| Cottagecore | Romantic & Natural | Cream, Sage, Dusty Rose | Free People, Spell |
| Y2K | Retro Futuristic | Silver, Baby Pink, Sky Blue | Von Dutch, Juicy Couture |

---

# CONCLUSION

vougeabulary demonstrates how AI concepts can be applied to solve a real, everyday problem in a structured and logical way. The system successfully integrates:

- **Intelligent filtering** (weather + occasion dual-condition logic)
- **Color theory** (group-based compatibility scoring)
- **Conversational AI** (personality-adaptive chatbot)
- **Data management** (persistent digital wardrobe)
- **Shopping discovery** (style-curated external search links)

As a prototype, the project prioritizes demonstrating clarity of thought, well-defined logic, and a complete user experience over technical complexity. The architecture is designed to be extensible — each module can be upgraded independently as the project evolves toward a production application.
