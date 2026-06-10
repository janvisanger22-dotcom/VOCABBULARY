"""
Style Profiles — vougeabulary
Defines all 8 fashion aesthetic profiles used across the app.
Used by: the AI chat system, the shop tab, and the recommendation UI.
"""

STYLE_PROFILES: dict[str, dict] = {
    "kawaii": {
        "name":        "Kawaii",
        "emoji":       "🎀",
        "tagline":     "Sweet & Dreamy",
        "description": "Pastel Japanese cuteness with frills, bows, and sugary details",
        "accent":      "#FFB7C5",
        "colors":      ["pink", "white", "lavender", "mint", "cream"],
        "palette_hex": ["#FFB7C5", "#FFFFFF", "#C9B1FF", "#B5EAD7", "#FFF9E6"],
        "keywords":    ["pastel", "cute", "frilly", "bow", "dreamy", "lolita"],
        "brands":      ["Angelic Pretty", "Baby The Stars Shine Bright", "Swimmer", "Lazy Oaf"],
        "searches":    ["kawaii fashion clothes", "pastel cute outfit", "sweet lolita dress"],
        "chat_tone":   "bubbly and enthusiastic — use 🎀, lots of cute words",
    },
    "gyaru": {
        "name":        "Gyaru",
        "emoji":       "💅",
        "tagline":     "Glam & Fierce",
        "description": "Bold Japanese street glamour with dramatic flair and unapologetic confidence",
        "accent":      "#FF69B4",
        "colors":      ["white", "coral", "gold", "tan", "hot pink"],
        "palette_hex": ["#FFFFFF", "#FF7F7F", "#FFD700", "#D2691E", "#FF69B4"],
        "keywords":    ["glam", "flashy", "dramatic", "fierce", "bold"],
        "brands":      ["MOUSSY", "SLY", "Liz Lisa", "COCOLULU"],
        "searches":    ["gyaru gal fashion style", "japanese glamour outfit", "gal kei clothes"],
        "chat_tone":   "confident, glamorous, encouraging — use 💅",
    },
    "emo": {
        "name":        "Emo",
        "emoji":       "🖤",
        "tagline":     "Dark & Expressive",
        "description": "Emotionally raw alternative fashion with dark palette and edge",
        "accent":      "#9B59B6",
        "colors":      ["black", "dark red", "grey", "deep purple"],
        "palette_hex": ["#1A1A1A", "#8B0000", "#666666", "#4B0082"],
        "keywords":    ["dark", "band tee", "edgy", "alternative", "chains", "fishnet"],
        "brands":      ["Killstar", "Disturbia", "Hot Topic", "Drop Dead"],
        "searches":    ["emo alt fashion clothes", "dark aesthetic outfit", "gothic alternative clothing"],
        "chat_tone":   "poetic, a little dramatic, dark humor — use 🖤",
    },
    "minimalist": {
        "name":        "Minimalist",
        "emoji":       "◻",
        "tagline":     "Clean & Elevated",
        "description": "Understated elegance through clean lines, neutral tones, and timeless quality",
        "accent":      "#C8B89A",
        "colors":      ["white", "black", "grey", "beige", "cream"],
        "palette_hex": ["#FFFFFF", "#1A1A1A", "#888888", "#C8B89A", "#FFF8E1"],
        "keywords":    ["clean", "simple", "neutral", "structured", "capsule", "timeless"],
        "brands":      ["COS", "Everlane", "Uniqlo", "Muji", "Arket", "The Row"],
        "searches":    ["minimalist capsule wardrobe", "clean aesthetic outfit", "neutral style clothes"],
        "chat_tone":   "precise, calm, no unnecessary words — clean sentences",
    },
    "formal": {
        "name":        "Formal",
        "emoji":       "🎩",
        "tagline":     "Sharp & Sophisticated",
        "description": "Polished professional attire that commands presence and radiates confidence",
        "accent":      "#4A90D9",
        "colors":      ["black", "navy", "white", "charcoal", "burgundy"],
        "palette_hex": ["#1A1A1A", "#1B2A4A", "#FFFFFF", "#333333", "#800020"],
        "keywords":    ["suit", "blazer", "tailored", "professional", "sharp", "power dressing"],
        "brands":      ["Hugo Boss", "Zara", "Massimo Dutti", "Theory", "Banana Republic"],
        "searches":    ["formal professional outfit", "power dressing clothes", "business fashion look"],
        "chat_tone":   "professional, direct, authoritative — no fluff",
    },
    "streetwear": {
        "name":        "Streetwear",
        "emoji":       "🧢",
        "tagline":     "Urban & Bold",
        "description": "Street-born culture with graphic tees, sneakers, and oversized silhouettes",
        "accent":      "#E74C3C",
        "colors":      ["black", "white", "grey", "red", "olive"],
        "palette_hex": ["#1A1A1A", "#FFFFFF", "#666666", "#CC0000", "#556B2F"],
        "keywords":    ["hoodie", "graphic tee", "oversized", "urban", "hype", "sneakers"],
        "brands":      ["Supreme", "Off-White", "Palace", "Stussy", "Carhartt WIP"],
        "searches":    ["streetwear hype fashion", "urban style outfit", "sneakerhead fashion"],
        "chat_tone":   "casual, cool, hype language — use 🔥",
    },
    "cottagecore": {
        "name":        "Cottagecore",
        "emoji":       "🌿",
        "tagline":     "Romantic & Natural",
        "description": "Nature-inspired romanticism with florals, linen, and pastoral charm",
        "accent":      "#87A878",
        "colors":      ["cream", "sage green", "dusty rose", "warm brown", "butter yellow"],
        "palette_hex": ["#FFF8E1", "#87A878", "#D4A0A0", "#8B6914", "#F5E642"],
        "keywords":    ["floral", "linen", "vintage", "nature", "pastoral", "romantic"],
        "brands":      ["Free People", "Anthropologie", "Spell", "Faithfull The Brand"],
        "searches":    ["cottagecore aesthetic fashion", "romantic floral dress", "prairie vintage style"],
        "chat_tone":   "gentle, dreamy, nature metaphors — use 🌿🌸",
    },
    "y2k": {
        "name":        "Y2K",
        "emoji":       "✨",
        "tagline":     "Retro Futuristic",
        "description": "Early 2000s fashion revival with bold colors, low-rise fits, and nostalgia",
        "accent":      "#DDA0DD",
        "colors":      ["silver", "baby pink", "sky blue", "white", "holographic"],
        "palette_hex": ["#C0C0C0", "#FFB6C1", "#87CEEB", "#FFFFFF", "#DDA0DD"],
        "keywords":    ["y2k", "2000s", "low rise", "butterfly", "glitter", "bedazzled"],
        "brands":      ["ASOS", "Von Dutch", "Juicy Couture", "PrettyLittleThing"],
        "searches":    ["y2k fashion aesthetic", "2000s style comeback", "retro futuristic outfit"],
        "chat_tone":   "enthusiastic, nostalgic, bestie energy — use ✨",
    },
}


def get_style(key: str) -> dict:
    """Return a style profile by key. Defaults to minimalist if not found."""
    return STYLE_PROFILES.get(key, STYLE_PROFILES["minimalist"])


def all_style_keys() -> list[str]:
    return list(STYLE_PROFILES.keys())


def shopping_links(key: str) -> list[dict]:
    """Generate shopping search links for a given style."""
    p = get_style(key)
    return [
        {
            "term":      term,
            "google":    f"https://www.google.com/search?q={term.replace(' ','+')}",
            "asos":      f"https://www.asos.com/search/?q={term.replace(' ','+')}",
            "pinterest": f"https://www.pinterest.com/search/pins/?q={term.replace(' ','+')}",
            "depop":     f"https://www.depop.com/search/?q={term.replace(' ','+')}",
        }
        for term in p["searches"]
    ]
