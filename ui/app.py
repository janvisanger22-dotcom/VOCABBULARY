import sys, os, json, random, base64, re
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai'))
from clothing_item import ClothingItem, Category, Occasion, Weather, Wardrobe
from recommendation_engine import RecommendationEngine
from color_rules import color_compatibility_score

try:
    from groq import Groq as GroqClient
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'vouge-luxury-secret-2024')

# Set your Google Client ID here for local development, or use the env var on Render
_LOCAL_GOOGLE_CLIENT_ID = ''  # paste your Client ID between the quotes

DATA_DIR         = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
WARDROBE_FILE    = os.path.join(DATA_DIR, 'wardrobe.json')   # default items for new users
WARDROBES_FILE   = os.path.join(DATA_DIR, 'wardrobes.json')  # per-user wardrobes
SAVED_FITS_FILE  = os.path.join(DATA_DIR, 'saved_fits_db.json')
USERS_FILE       = os.path.join(DATA_DIR, 'users.json')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ── Style profiles ─────────────────────────────────────────────────────────────
STYLES = {
    "kawaii":      {"name":"Kawaii",      "emoji":"🎀","tagline":"Sweet & Dreamy",       "accent":"#FFB7C5","description":"Pastel Japanese cuteness with frills, bows, and sugary details","colors":["pink","white","lavender","mint","cream"],"hex":["#FFB7C5","#FFFFFF","#C9B1FF","#B5EAD7","#FFF9E6"],"keywords":["pastel","cute","frilly","bow","dreamy"],"brands":["Angelic Pretty","Swimmer","Lazy Oaf","Baby The Stars Shine Bright"],"searches":["kawaii fashion clothes","pastel cute outfit","sweet lolita dress"]},
    "gyaru":       {"name":"Gyaru",       "emoji":"💅","tagline":"Glam & Fierce",         "accent":"#FF69B4","description":"Bold Japanese street glamour with dramatic flair and unapologetic confidence","colors":["white","coral","gold","tan","hot pink"],"hex":["#FFFFFF","#FF7F7F","#FFD700","#D2691E","#FF69B4"],"keywords":["glam","flashy","dramatic","fierce","bold"],"brands":["MOUSSY","SLY","Liz Lisa","COCOLULU"],"searches":["gyaru gal fashion style","japanese glamour outfit","gal kei clothes"]},
    "emo":         {"name":"Emo",         "emoji":"🖤","tagline":"Dark & Expressive",     "accent":"#9B59B6","description":"Emotionally raw alternative fashion with dark palette and edge","colors":["black","dark red","grey","deep purple"],"hex":["#1A1A1A","#8B0000","#666666","#4B0082"],"keywords":["dark","band tee","edgy","alternative","chains"],"brands":["Killstar","Disturbia","Hot Topic","Drop Dead"],"searches":["emo alt fashion clothes","dark aesthetic outfit","gothic alternative clothing"]},
    "minimalist":  {"name":"Minimalist",  "emoji":"◻","tagline":"Clean & Elevated",      "accent":"#C8B89A","description":"Understated elegance through clean lines, neutral tones, and timeless quality","colors":["white","black","grey","beige","cream"],"hex":["#FFFFFF","#1A1A1A","#888888","#C8B89A","#FFF8E1"],"keywords":["clean","simple","neutral","structured","capsule"],"brands":["COS","Everlane","Uniqlo","Muji","Arket"],"searches":["minimalist capsule wardrobe","clean aesthetic outfit","neutral style clothes"]},
    "formal":      {"name":"Formal",      "emoji":"🎩","tagline":"Sharp & Sophisticated", "accent":"#4A90D9","description":"Polished professional attire that commands presence and radiates confidence","colors":["black","navy","white","charcoal","burgundy"],"hex":["#1A1A1A","#1B2A4A","#FFFFFF","#333333","#800020"],"keywords":["suit","blazer","tailored","professional","sharp"],"brands":["Hugo Boss","Zara","Massimo Dutti","Theory"],"searches":["formal professional outfit","power dressing clothes","business fashion look"]},
    "streetwear":  {"name":"Streetwear",  "emoji":"🧢","tagline":"Urban & Bold",          "accent":"#E74C3C","description":"Street-born culture with graphic tees, sneakers, and oversized silhouettes","colors":["black","white","grey","red","olive"],"hex":["#1A1A1A","#FFFFFF","#666666","#CC0000","#556B2F"],"keywords":["hoodie","graphic tee","oversized","urban","hype"],"brands":["Supreme","Off-White","Palace","Stussy","Carhartt"],"searches":["streetwear hype fashion","urban style outfit","sneakerhead fashion"]},
    "cottagecore": {"name":"Cottagecore", "emoji":"🌿","tagline":"Romantic & Natural",    "accent":"#87A878","description":"Nature-inspired romanticism with florals, linen, and pastoral charm","colors":["cream","sage green","dusty rose","warm brown","butter yellow"],"hex":["#FFF8E1","#87A878","#D4A0A0","#8B6914","#F5E642"],"keywords":["floral","linen","vintage","nature","pastoral"],"brands":["Free People","Anthropologie","Spell","Faithfull"],"searches":["cottagecore aesthetic fashion","romantic floral dress","prairie vintage style"]},
    "y2k":         {"name":"Y2K",         "emoji":"✨","tagline":"Retro Futuristic",       "accent":"#DDA0DD","description":"Early 2000s fashion revival with bold colors, low-rise fits, and nostalgia","colors":["silver","baby pink","sky blue","white","holographic"],"hex":["#C0C0C0","#FFB6C1","#87CEEB","#FFFFFF","#DDA0DD"],"keywords":["y2k","2000s","low rise","butterfly","glitter"],"brands":["ASOS","Von Dutch","Juicy Couture","PrettyLittleThing"],"searches":["y2k fashion aesthetic","2000s style comeback","retro futuristic outfit"]},
}

# ── Color seasons ──────────────────────────────────────────────────────────────
COLOR_SEASONS = {
    "spring": {
        "name": "Spring", "emoji": "🌸", "tagline": "Warm, Clear & Light",
        "description": "Springs have warm golden undertones with a fresh, clear appearance. Your coloring is light-to-medium with a peachy or golden warmth.",
        "undertone": "Warm",
        "traits": ["Warm peachy or golden skin", "Golden blonde, strawberry blonde, or warm light brown hair", "Blue, green, turquoise, or golden-brown eyes"],
        "best_colors": ["coral", "warm peach", "ivory", "warm yellow", "light green", "turquoise", "camel", "warm orange"],
        "avoid": ["icy pastels", "cool grey", "pure black", "cool blue-red"],
        "palette_hex": ["#FFB347", "#FFDAB9", "#FFF5DC", "#90EE90", "#20B2AA", "#DEB887", "#FF7F50", "#F0E68C"],
        "palette_names": ["warm coral", "peach", "ivory", "light green", "turquoise", "camel", "orange", "warm yellow"],
        "neutrals": ["ivory", "camel", "warm beige", "warm white", "light warm brown"],
        "accent": "#FFB347",
        "style_tip": "Wear warm, clear colors near your face. Cream works better than stark white. Avoid icy or grey-toned shades — they wash you out.",
        "celebrities": ["Taylor Swift", "Emma Stone", "Nicole Kidman"],
    },
    "summer": {
        "name": "Summer", "emoji": "🌊", "tagline": "Cool, Soft & Muted",
        "description": "Summers have cool undertones with soft, muted coloring. Think powdery, blended tones rather than vivid — your palette is delicate and refined.",
        "undertone": "Cool",
        "traits": ["Cool pink, rosy, or light beige skin", "Ash blonde, light brown, or platinum hair", "Blue, grey, soft green, or violet eyes"],
        "best_colors": ["dusty rose", "lavender", "powder blue", "cool grey", "raspberry", "soft plum", "mauve", "soft navy"],
        "avoid": ["orange", "warm yellow", "warm brown", "bright orange-red", "olive"],
        "palette_hex": ["#FFB6C1", "#E6E6FA", "#87CEEB", "#C0C0C0", "#E75480", "#9370DB", "#B0C4DE", "#D8BFD8"],
        "palette_names": ["dusty rose", "lavender", "powder blue", "silver grey", "raspberry", "plum", "steel blue", "thistle"],
        "neutrals": ["cool grey", "soft white", "blue-grey", "dusty taupe", "soft navy"],
        "accent": "#B0C4DE",
        "style_tip": "Pure white can overpower you — opt for soft white or cream. Dusty, muted tones in cool shades are your signature palette.",
        "celebrities": ["Cate Blanchett", "Gwyneth Paltrow", "Jennifer Aniston"],
    },
    "autumn": {
        "name": "Autumn", "emoji": "🍂", "tagline": "Warm, Rich & Earthy",
        "description": "Autumns have deep warm undertones with rich, earthy coloring. Your palette is golden, muted, and intensely warm — like a forest in October.",
        "undertone": "Warm",
        "traits": ["Warm golden, olive, bronze, or dark skin", "Red, auburn, copper, dark brown, or chestnut hair", "Brown, amber, hazel, warm green, or golden eyes"],
        "best_colors": ["rust", "burnt orange", "olive", "mustard", "warm brown", "forest green", "teal", "brick red", "cream"],
        "avoid": ["icy pastels", "cool pink", "baby blue", "pure white", "cool grey"],
        "palette_hex": ["#B7410E", "#E67E22", "#6B7C3A", "#C8A82A", "#8B4513", "#2E8B57", "#CD853F", "#A0522D"],
        "palette_names": ["rust", "burnt orange", "olive", "mustard", "chocolate", "forest green", "caramel", "sienna"],
        "neutrals": ["camel", "chocolate brown", "warm beige", "olive", "dark chocolate", "warm cream"],
        "accent": "#C8A82A",
        "style_tip": "Wear rich earthy tones head-to-toe — they enhance your depth. Gold jewellery always, never silver. Avoid anything icy or cool-toned.",
        "celebrities": ["Julia Roberts", "Julianne Moore", "Beyoncé"],
    },
    "winter": {
        "name": "Winter", "emoji": "❄️", "tagline": "Cool, Clear & High Contrast",
        "description": "Winters have cool undertones with high-contrast, vivid coloring. Your palette is pure, intense, and dramatic — no muddy or muted tones.",
        "undertone": "Cool",
        "traits": ["Cool olive, cool beige, medium, or deep dark skin", "Dark brown, black, or very dark hair", "Dark brown, black, vivid blue, or green eyes"],
        "best_colors": ["pure white", "true black", "cobalt blue", "emerald green", "magenta", "royal purple", "true red", "icy pink"],
        "avoid": ["orange", "warm beige", "camel", "mustard", "warm brown", "muted pastels"],
        "palette_hex": ["#FFFFFF", "#1A1A1A", "#0047AB", "#50C878", "#FF00FF", "#7B2FBE", "#CC0000", "#E8D5E8"],
        "palette_names": ["pure white", "true black", "cobalt blue", "emerald", "magenta", "royal purple", "true red", "icy pink"],
        "neutrals": ["pure white", "true black", "charcoal grey", "cool navy", "icy grey"],
        "accent": "#0047AB",
        "style_tip": "High contrast is your power move — pair stark white with black. Avoid anything warm or muted near your face; it dulls your natural brightness.",
        "celebrities": ["Lupita Nyong'o", "Dua Lipa", "Priyanka Chopra"],
    },
}

# ── Body types ─────────────────────────────────────────────────────────────────
BODY_TYPES = {
    "hourglass": {
        "name": "Hourglass", "emoji": "⌛",
        "tagline": "Balanced & Defined",
        "description": "Bust and hips are roughly equal in width with a clearly defined, smaller waist. Your proportions are naturally balanced.",
        "goal": "Accentuate your natural waist and highlight your balanced proportions",
        "do_wear": ["Wrap dresses and tops", "Belted clothing at the waist", "Fit-and-flare silhouettes", "High-waisted bottoms", "Bodycon and fitted styles", "V-necks and scoop necks", "Pencil skirts"],
        "avoid": ["Boxy or oversized tops that hide your waist", "Shapeless shift dresses", "Low-rise bottoms that cut at the widest part", "Stiff fabrics that don't follow your shape"],
        "best_cuts": ["Wrap", "Fit-and-flare", "Bodycon", "Pencil skirt", "Sheath dress"],
        "tips": "Your natural waist is your best feature — always define it. Structured fabrics and wrap styles work beautifully on you.",
        "outfit_ideas": ["Wrap midi dress + block heels", "High-waist jeans + fitted turtleneck + belt", "Bodycon skirt + tucked blouse"],
        "accent": "#FF6B9D",
    },
    "pear": {
        "name": "Pear / Triangle", "emoji": "🍐",
        "tagline": "Draw the Eye Upward",
        "description": "Hips and thighs are wider than your shoulders. Your lower body is more prominent, with a smaller waist and narrower upper body.",
        "goal": "Balance proportions by drawing attention upward to the shoulders and bust",
        "do_wear": ["Structured tops with volume or embellishment", "Boat necks and wide necklines", "Bright or patterned tops, dark plain bottoms", "A-line and flared skirts", "Bootcut and wide-leg trousers", "Off-shoulder and puff-sleeve tops"],
        "avoid": ["Skinny jeans with plain dark tops (draws eye down)", "Tight pencil skirts", "Cargo pockets on hips", "Horizontal stripes on the hip area", "Pleated trousers"],
        "best_cuts": ["A-line skirt", "Bootcut trousers", "Peplum tops", "Empire waist", "Wide-leg pants"],
        "tips": "Bold colours, prints, and structure on top — your upper half is where the eye should go. Keep bottoms simple and dark.",
        "outfit_ideas": ["Bold printed top + dark straight-leg trousers", "Off-shoulder blouse + A-line midi skirt", "Structured blazer + slim dark jeans"],
        "accent": "#27AE60",
    },
    "apple": {
        "name": "Apple / Oval", "emoji": "🍎",
        "tagline": "Elongate & Streamline",
        "description": "Weight tends to sit around your midsection. Shoulders may be broader, bust often larger. Your legs and arms are usually slimmer.",
        "goal": "Elongate the torso, minimize the midsection, and show off your great legs",
        "do_wear": ["V-necks and deep necklines that draw the eye down", "Empire-waist tops and dresses", "Flowy tunics over leggings", "Monochrome outfit (same color head-to-toe)", "Vertical stripes", "A-line and wrap dresses", "Straight-leg or bootcut trousers"],
        "avoid": ["Clingy fabrics across the stomach", "Wide belts at the natural waist", "Horizontal stripes in the middle", "Cropped tops", "High-waisted anything without a flowy layer"],
        "best_cuts": ["Empire waist", "A-line dress", "Shift dress", "Tunic over straight pants", "Wrap dress"],
        "tips": "Vertical lines are your best friend — they elongate. Monochrome looks are incredibly powerful on you. Show off your legs whenever possible!",
        "outfit_ideas": ["Flowy tunic + straight trousers + block heels", "Wrap dress + ankle boots", "V-neck blouse + wide-leg pants (same color family)"],
        "accent": "#E74C3C",
    },
    "rectangle": {
        "name": "Rectangle / Banana", "emoji": "📐",
        "tagline": "Create Curves & Dimension",
        "description": "Bust, waist, and hips are similar in width. Straight silhouette with minimal waist definition. Often athletic or lean-looking.",
        "goal": "Create the illusion of curves and add dimension and visual interest to your frame",
        "do_wear": ["Peplum tops that flare at the waist", "Ruffles, frills, and volume", "Belted outfits to create a waist", "Full and skater skirts", "Layered and textured pieces", "Horizontal stripes", "Wrap and draped styles"],
        "avoid": ["Completely straight, shapeless outfits from neck to hem", "Baggy clothes with no shape", "Vertical stripes head-to-toe (emphasises the straight line)"],
        "best_cuts": ["Peplum", "Fit-and-flare", "Wrap dress", "Skater skirt", "Belted trench coat"],
        "tips": "Add texture, layers, and visual interest. A belt can completely transform a straight silhouette. Ruffles and peplums are your secret weapon.",
        "outfit_ideas": ["Peplum top + skinny jeans + heels", "Full skater skirt + fitted top + wide belt", "Wrap dress with defined waist"],
        "accent": "#9B59B6",
    },
    "inverted_triangle": {
        "name": "Inverted Triangle", "emoji": "🔻",
        "tagline": "Balance Your Proportions",
        "description": "Shoulders are broader than your hips. Strong, athletic upper body. Narrow hips and waist. Often described as having a 'swimmer's build'.",
        "goal": "Balance broad shoulders by drawing attention downward and adding volume to the lower half",
        "do_wear": ["Wide-leg and flared trousers", "A-line and full skirts", "V-necks (draws eye down)", "Simple, minimal tops", "Flared jeans and bootcut", "Bold patterns and colors on the bottom", "Low-rise bottoms"],
        "avoid": ["Off-shoulder and cold-shoulder tops", "Padded or structured shoulders", "Boat necks", "Bold prints or embellishments on top", "Halter tops", "Strapless styles"],
        "best_cuts": ["Wide-leg trousers", "A-line skirt", "Bootcut jeans", "Maxi skirts", "Flared jeans"],
        "tips": "Keep your top half simple and minimal — let the bottom half do the talking. The goal is to create a balanced triangle shape.",
        "outfit_ideas": ["Simple tee + wide-leg floral trousers", "V-neck top + A-line midi skirt", "Fitted top + bold-print maxi skirt"],
        "accent": "#E67E22",
    },
}

# ── Color hex map ──────────────────────────────────────────────────────────────
COLOR_HEX = {
    "white":"#FFFFFF","black":"#222222","grey":"#888888","gray":"#888888","beige":"#C8B89A",
    "navy":"#1B2A4A","cream":"#FFF8E1","camel":"#C19A6B","red":"#C0392B","orange":"#E67E22",
    "yellow":"#F1C40F","pink":"#FF9EB5","coral":"#FF6B6B","burgundy":"#800020","maroon":"#800000",
    "blue":"#2980B9","green":"#27AE60","purple":"#8E44AD","teal":"#16A085","mint":"#A8E6CF",
    "lavender":"#C9B1FF","cyan":"#00BCD4","brown":"#6D4C41","olive":"#6B7C3A","mustard":"#C8A82A",
    "rust":"#B7410E","tan":"#D2B48C","khaki":"#C3B091","silver":"#C0C0C0","gold":"#FFD700",
    "dark red":"#8B0000","deep purple":"#4B0082","charcoal":"#333333","hot pink":"#FF69B4",
    "sage green":"#87A878","dusty rose":"#D4A0A0","butter yellow":"#F5E642","sky blue":"#87CEEB",
    "baby pink":"#FFB6C1","holographic":"#DDA0DD","ivory":"#FFF5DC","warm peach":"#FFDAB9",
    "burnt orange":"#CC5500","forest green":"#228B22","cobalt blue":"#0047AB","emerald":"#50C878",
    "magenta":"#FF00FF","royal purple":"#7B2FBE","icy pink":"#FFD1DC","powder blue":"#B0C4DE",
    "dusty rose":"#D4A0A0","mauve":"#E0B0FF","raspberry":"#E75480","plum":"#8E4585",
}

# ── Data helpers ───────────────────────────────────────────────────────────────
def _wardrobes():
    if os.path.exists(WARDROBES_FILE):
        with open(WARDROBES_FILE) as f: return json.load(f)
    return {}

def _save_wardrobes(db):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(WARDROBES_FILE, 'w') as f: json.dump(db, f, indent=2)

def load_wardrobe():
    user = session.get('username', 'guest')
    db   = _wardrobes()
    if user not in db:
        default = json.load(open(WARDROBE_FILE)) if os.path.exists(WARDROBE_FILE) else []
        db[user] = default
        _save_wardrobes(db)
    return db[user]

def save_wardrobe(items):
    user = session.get('username', 'guest')
    db   = _wardrobes()
    db[user] = items
    _save_wardrobes(db)

def _fits_db():
    if os.path.exists(SAVED_FITS_FILE):
        with open(SAVED_FITS_FILE) as f: return json.load(f)
    return {}

def load_saved_fits():
    user = session.get('username', 'guest')
    return _fits_db().get(user, [])

def save_saved_fits(fits):
    user = session.get('username', 'guest')
    db   = _fits_db()
    db[user] = fits
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SAVED_FITS_FILE, 'w') as f: json.dump(db, f, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f: return json.load(f)
    return {}

def save_users(users):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, 'w') as f: json.dump(users, f, indent=2)

def to_engine(items):
    w = Wardrobe()
    for i in items:
        try:
            w.add_item(ClothingItem(
                item_id=i['id'], name=i['name'],
                category=Category(i['category']), color=i['color'].lower(),
                occasions=[Occasion(o) for o in i['occasions']],
                weather_suitability=[Weather(x) for x in i['weather']],
                is_clean=i.get('is_clean', True)
            ))
        except Exception: pass
    return w

# ── Outfit verdict logic ───────────────────────────────────────────────────────
def compute_verdict(items: list) -> dict:
    """Rule-based verdict for a user-built outfit."""
    if not items: return {"score": 0, "summary": "No items selected.", "strengths": [], "suggestions": []}

    colors = [i['color'] for i in items]
    names  = [i['name']  for i in items]

    # Color harmony scores for all pairs
    pairs, pair_scores = [], []
    for a in range(len(colors)):
        for b in range(a+1, len(colors)):
            s = color_compatibility_score(colors[a], colors[b])
            pairs.append((names[a], names[b], s))
            pair_scores.append(s)

    avg_color = sum(pair_scores) / len(pair_scores) if pair_scores else 1.0
    score = round(avg_color * 100)

    # Build strengths and suggestions
    strengths, suggestions = [], []

    if avg_color >= 0.85:
        strengths.append("Excellent color harmony — all pieces work beautifully together")
    elif avg_color >= 0.70:
        strengths.append("Good color compatibility overall")
    else:
        suggestions.append("Color pairing could be stronger — try replacing one item with a neutral (black, white, beige, navy)")

    # Check for clashing pairs
    clashes = [(a, b) for a, b, s in pairs if s < 0.50]
    for a, b in clashes:
        suggestions.append(f"Consider swapping: {a} and {b} clash tonally")

    # Check variety
    categories = [i.get('category','') for i in items]
    if 'shoes' not in categories:
        suggestions.append("Add shoes to complete the look")
    if len(set(colors)) == 1:
        strengths.append("Bold monochrome look — very intentional and chic")

    # Summary
    if score >= 85:
        summary = "This outfit is a winner — strong color harmony and great overall balance."
    elif score >= 65:
        summary = "Solid outfit with good potential. Minor adjustments could elevate it further."
    elif score >= 45:
        summary = "The concept is there, but some pieces are competing. Consider swapping one item."
    else:
        summary = "This combination needs work — the colors are clashing. A neutral swap will fix most of it."

    if not strengths:
        strengths.append("Outfit has been put together — now just refine the color pairing")

    return {"score": score, "summary": summary, "strengths": strengths, "suggestions": suggestions}

# ── Rule-based chat ────────────────────────────────────────────────────────────
def rule_chat(msg, style, wardrobe, color_season=None, body_type=None):
    p  = STYLES.get(style, STYLES['minimalist'])
    ml = msg.lower().strip()

    # ── intent flags (whole-word safe) ────────────────────────────────────────
    def has(text, *phrases):
        """Return True if any phrase matches as a whole word/phrase in text."""
        for ph in phrases:
            if re.search(r'(?<!\w)' + re.escape(ph) + r'(?!\w)', text):
                return True
        return False

    greet    = has(ml,'hi','hello','hey','sup','yo','hii','hola','howdy',
                       'how are','how r u','how r you','good morning','good evening','good night',
                       'wassup',"what's up",'whats up')
    feeling  = has(ml,'how are','how r','feeling','doing','fine','good','great','bad','okay','ok')
    outfit   = has(ml,'wear','outfit','suggest','recommend','style me','what should',
                       'what to wear','look','pick','put together','match')
    occasion = has(ml,'party','date','wedding','work','office','gym','sport','beach',
                       'formal','casual','night out','brunch','school','college','interview',
                       'festival','concert','dinner','event','birthday','going out')
    shop     = has(ml,'buy','shop','shopping','purchase','find','where to get','order','store','online')
    colors   = has(ml,'color','colour','palette','season','shade','tone','hue')
    tip      = has(ml,'tip','advice','how to','help','guide','trick','hack','rule')
    body_q   = has(ml,'body','shape','figure','flatter','slim','frame','body type')
    wardrobe_q = has(ml,'wardrobe','closet','clothes','clothing','what do i have','what i own')
    accessory_q= has(ml,'accessory','bag','shoes','jewel','necklace','earring','belt','hat','scarf')
    thank    = has(ml,'thank','thanks','thx','perfect','love it','amazing','awesome','that helped')
    negative = has(ml,'nah','not really','boring','meh','ugly','hate','dislike','dont like',"don't like")

    # ── profile context suffix ─────────────────────────────────────────────────
    profile_ctx = ""
    cs_data, bt_data = None, None
    if color_season and color_season in COLOR_SEASONS:
        cs_data = COLOR_SEASONS[color_season]
        profile_ctx += f" As a **{cs_data['name']}** season, lean into {cs_data['best_colors'][0]} tones."
    if body_type and body_type in BODY_TYPES:
        bt_data = BODY_TYPES[body_type]

    # ── wardrobe items by occasion ─────────────────────────────────────────────
    def wardrobe_pick(occ_filter=None):
        pool = [i for i in wardrobe if not occ_filter or occ_filter in i.get('occasions',[])]
        if not pool: pool = wardrobe
        if not pool: return None
        return random.sample(pool, min(3, len(pool)))

    # ── responses — occasion first so "party/night out" beats "greet" ──────────

    if body_q and bt_data:
        do  = ', '.join(bt_data['do_wear'][:3])
        av  = bt_data['avoid'][0]
        return f"For your **{bt_data['name']}** body type — goal: {bt_data['goal']}. **Wear:** {do}. **Skip:** {av}. {bt_data['tips']}"

    if colors and cs_data:
        bc = ', '.join(f"**{c}**" for c in cs_data['best_colors'][:4])
        return f"As a **{cs_data['name']}** season — your power colors are: {bc}. {cs_data['style_tip']} Avoid: {', '.join(cs_data['avoid'][:2])}."

    # Occasion check runs before greet so "night out / party / wedding" don't get swallowed
    if occasion:
        occ_map = {'party':'party','date':'party','night out':'party','birthday':'party',
                   'work':'work','office':'work','interview':'work',
                   'wedding':'formal','formal':'formal','dinner':'formal',
                   'gym':'sport','sport':'sport','beach':'casual',
                   'school':'casual','college':'casual','brunch':'casual','festival':'casual','concert':'casual'}
        matched_occ = next((occ_map[k] for k in occ_map if k in ml), 'casual')
        picks = wardrobe_pick(matched_occ)
        occ_tips = {
            'party':   {'kawaii':"Go all out — sequins, pastels, bows 🎀",'emo':"Dark velvet or a band tee with fishnets 🖤",'minimalist':"A sleek monochrome set — let the cut do the talking.",'streetwear':"Statement sneakers + an oversized graphic tee 🔥",'cottagecore':"A floral midi with puffed sleeves 🌸",'y2k':"Metallic mini + platform heels, obviously ✨",'gyaru':"Go full glam — the bolder the better 💅",'formal':"A sharp blazer dress or tailored suit."},
            'work':    {'kawaii':"Soft pastels in structured silhouettes — office cute! 🎀",'emo':"Dark tailored pieces — professional with edge 🖤",'minimalist':"A crisp white shirt + well-fitted trousers. Nothing more needed.",'streetwear':"Clean sneakers + tidy joggers + a structured jacket 🧢",'cottagecore':"Linen blouse + wide-leg trousers in earthy tones 🌿",'y2k':"Low-rise trousers + a fitted cardigan ✨",'gyaru':"Polished glam — fitted blazer, heels, done 💅",'formal':"Classic navy or charcoal suit with quality leather shoes."},
            'formal':  {'kawaii':"A pastel ball gown or sweet A-line 🎀",'emo':"All-black formal — a tailored suit or long dark gown 🖤",'minimalist':"A column dress or perfectly cut suit in ivory or black.",'streetwear':"An elevated monochrome look — it's giving fashion week 🔥",'cottagecore':"A floral maxi with delicate details 🌸",'y2k':"A glamorous two-piece set or slinky slip dress ✨",'gyaru':"Full glam evening look — drama is the dress code 💅",'formal':"Tailored suit or floor-length gown. Clean, sharp, authoritative."},
            'casual':  {'kawaii':"Comfy pastels — cute hoodie + mini skirt 🎀",'emo':"Ripped jeans + band tee + boots 🖤",'minimalist':"White tee + straight-leg jeans + clean sneakers. Done.",'streetwear':"Oversized hoodie + cargo pants 🧢",'cottagecore':"A flowy blouse + linen trousers 🌿",'y2k':"Crop top + low-rise jeans + chunky trainers ✨",'gyaru':"Cute casual — mini skirt + fitted top 💅",'formal':"Smart casual — a blazer over a simple tee goes far."},
            'sport':   {'kawaii':None,'emo':None,'minimalist':"Monochrome activewear — black set or grey. Clean.",'streetwear':"Matching tracksuit or oversized tee + joggers 🔥",'cottagecore':None,'y2k':None,'gyaru':None,'formal':None},
        }
        tip_str = (occ_tips.get(matched_occ,{}).get(style) or f"Pick your best {p['colors'][0]} piece and build around it!")
        if picks:
            combo = " + ".join(f"**{x['name']}**" for x in picks[:2])
            return f"For a **{matched_occ}** occasion — from your wardrobe try: {combo}. {tip_str}{profile_ctx}"
        return f"For **{matched_occ}** — {tip_str}{profile_ctx} Add pieces in **My Wardrobe** to get outfit picks from your actual clothes!"

    if thank:
        resps = {'kawaii':"Yay, I'm so happy I could help!! 🎀",'emo':"...glad it worked. 🖤",'minimalist':"Good.",'streetwear':"Bet! Go off 🔥",'cottagecore':"Oh how wonderful, enjoy! 🌸",'y2k':"Omg yesss! Go be iconic ✨",'gyaru':"You're gonna slay, gorgeous 💅",'formal':"Excellent. You'll make a strong impression."}
        return resps.get(style, "Happy to help! Come back anytime 💫")

    if feeling and greet:
        resps = {'kawaii':"I'm always happy when I get to talk fashion!! 🎀 What cute look are we planning?",'emo':"Existing. 🖤 Let's channel that into a killer outfit — what's the vibe?",'minimalist':"Functioning. What are you dressing for today?",'streetwear':"Lowkey vibing 🧢 What are we putting together?",'cottagecore':"Floating through meadows thinking of florals 🌿 What's the occasion?",'y2k':"Living my best life bestie ✨ Tell me what we're wearing!",'gyaru':"Absolutely glowing 💅 Now let's make sure you are too — what's the plan?",'formal':"Very well, thank you. Now — what's the occasion?"}
        return resps.get(style, f"Doing great! I'm your {p['name']} AI stylist — what are we styling today? ✨")

    if greet:
        intros = {'kawaii':f"Kyaaa~ hiii!! 🎀 Ready to look super cute?{profile_ctx}",'emo':f"...hey. 🖤 What aesthetic are we crafting?{profile_ctx}",'minimalist':f"Hello. What are you dressing for today?{profile_ctx}",'streetwear':f"Yooo! 🧢 What are we cooking?{profile_ctx}",'cottagecore':f"Hello lovely! 🌿 What's the occasion?{profile_ctx}",'y2k':f"Omg hiii bestie!! ✨ What look are we building?{profile_ctx}",'gyaru':f"Heyyy gorgeous! 💅 Let's make you iconic. What's the plan?{profile_ctx}",'formal':f"Good day. What occasion are we dressing for?{profile_ctx}"}
        return intros.get(style, f"Hey! I'm your {p['name']} AI stylist ✨ What are we wearing?{profile_ctx}")

    if wardrobe_q:
        if not wardrobe:
            return "Your wardrobe is empty right now! Head to **My Wardrobe** tab to add your clothes — then I can suggest outfits from what you actually own 👗"
        cats = {}
        for i in wardrobe:
            cats.setdefault(i['category'], 0); cats[i['category']] += 1
        summary = ', '.join(f"{v} {k}{'s' if v>1 else ''}" for k,v in cats.items())
        return f"You have **{len(wardrobe)} items** in your wardrobe: {summary}. Want me to suggest an outfit from what you own?"

    if outfit:
        picks = wardrobe_pick()
        if not picks:
            return f"Your wardrobe is empty! Add clothes in **My Wardrobe** first, then I can suggest full looks 👗"
        combo = " + ".join(f"**{x['name']}**" for x in picks[:2])
        kw = random.choice(p['keywords'])
        cs_bonus = f" These work especially well for your {cs_data['name']} season palette." if cs_data else ""
        return f"From your wardrobe, try: {combo}. Keep it **{kw}**.{cs_bonus}{profile_ctx}"

    if shop:
        brand  = random.choice(p['brands'])
        term   = random.choice(p['searches'])
        link   = f"https://www.google.com/search?q={term.replace(' ','+')}"
        depop  = f"https://www.depop.com/search/?q={term.replace(' ','+')}"
        return f"For **{p['name']}** shopping — **{brand}** is a go-to. [Search Google]({link}) or find vintage on [Depop]({depop}) 🛍️{profile_ctx}"

    if accessory_q:
        acc_tips = {'kawaii':"Hair clips, bows, platform shoes, and layered cute necklaces 🎀",'emo':"Chunky boots, studded belts, fishnet socks, and chain necklaces 🖤",'minimalist':"One clean leather bag and minimal gold jewellery — nothing more.",'streetwear':"A fitted cap, chunky sneakers, and a crossbody bag 🧢",'cottagecore':"Straw hat, floral hair pins, and woven basket bag 🌿",'y2k':"Butterfly clips, mini bag, and platform trainers ✨",'gyaru':"Statement bag, sky-high heels, and dramatic lashes 💅",'formal':"Classic watch, leather belt, and quality leather shoes."}
        return acc_tips.get(style, f"For {p['name']}, accessories should complement your {p['colors'][0]} palette.") + (profile_ctx or "")

    if tip:
        tips = {'kawaii':"Layer pastels + mix textures — lace, velvet, chiffon. Accessories are everything 🎀",'emo':"Add deep purples and dark reds for dimension. Layer a band tee under flannel 🖤",'minimalist':"Invest in fit over quantity. One perfectly fitting piece beats five okay ones.",'streetwear':"Proportions are key — oversized top = slim bottom. Or both oversized for maximum drip 🧢",'cottagecore':"Thrift stores are goldmines for florals, linen, and vintage silhouettes 🌿",'y2k':"Low-rise + layered dainty jewellery instantly Y2Ks any outfit ✨",'gyaru':"Hair and makeup complete the look — it's 50% fashion, 50% glam 💅",'formal':"Shoes tell the story — invest in quality leather footwear before anything else."}
        base = tips.get(style, f"{p['description']}. Start with {p['colors'][0]} basics.")
        season_tip = f" Since you're a **{cs_data['name']}** season, gravitate toward {cs_data['best_colors'][0]} tones." if cs_data else ""
        return base + season_tip

    if negative:
        resps = {'kawaii':"Aww no worries!! 🎀 What vibe ARE we going for?","emo":"Dark. I respect it. 🖤 What does work for you?","minimalist":"Understood. What would you prefer instead?","streetwear":"Say less 🔥 What direction you thinking?","cottagecore":"Oh let's find something you love 🌿 What's your mood?","y2k":"Ok ok bestie ✨ What ARE we feeling then?","gyaru":"We pivot 💅 Tell me what speaks to your soul.","formal":"Duly noted. What would better suit your needs?"}
        return resps.get(style, "No problem — tell me more about what you're looking for!")

    # General fallback — varied, never the same twice
    fallbacks = {
        'kawaii':  ["Tell me the occasion and I'll make it SO cute 🎀","What aesthetic moment are we going for?? 🎀","Ooh what's the event? Tell me everything 🎀"],
        'emo':     ["What's the mood — full dark or subtly alt? 🖤","Tell me the vibe. I'll find the fit. 🖤","What are we expressing today? 🖤"],
        'minimalist':["What are you dressing for?","Tell me the occasion and I'll find the right piece.","What's the context — work, casual, or something special?"],
        'streetwear':["Cozy or clean? Day or night? 🔥","What's the fit goal — comfy or flexing? 🧢","Give me the occasion and I'll deliver 🔥"],
        'cottagecore':["Garden party, forest walk, or everyday fairy energy? 🌸","What's the occasion, lovely? 🌿","Tell me the vibe and I'll style you perfectly 🌸"],
        'y2k':     ["Britney 2003 or Paris Hilton chic? Both valid ✨","What's the occasion bestie? I have SO many ideas ✨","Tell me everything — where are we going?? ✨"],
        'gyaru':   ["Full glam or casual today, gorgeous? 💅","What's the event? I'll make you unforgettable 💅","Tell me the occasion and watch me work 💅"],
        'formal':  ["Boardroom, gala, or interview? Let me tailor the look.","What's the occasion? I'll dress you to impress.","Tell me the context and I'll find the perfect look."],
    }
    options = fallbacks.get(style, [f"Tell me more! I'm your {p['name']} style expert 💫"])
    return random.choice(options)

# ── Auth routes ────────────────────────────────────────────────────────────────
@app.route('/login')
def login_page():
    if 'username' in session:
        return redirect('/')
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '') or _LOCAL_GOOGLE_CLIENT_ID
    return render_template('login.html', google_client_id=google_client_id)

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    import urllib.request, urllib.error
    data  = request.json
    token = data.get('credential', '')
    if not token:
        return jsonify({'error': 'No credential provided'}), 400
    try:
        url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        with urllib.request.urlopen(url, timeout=5) as resp:
            info = json.loads(resp.read())
        email = info.get('email', '')
        name  = info.get('name', '') or info.get('given_name', '') or email.split('@')[0]
        if not email or not info.get('email_verified'):
            return jsonify({'error': 'Google account not verified'}), 401
        # Use email-derived username so the same Google account always maps to same user
        username = re.sub(r'[^a-z0-9_]', '_', email.lower())
        users = load_users()
        if username not in users:
            users[username] = {
                'password':     generate_password_hash(f'google_oauth_{email}'),
                'display_name': name,
                'email':        email,
                'provider':     'google',
            }
            save_users(users)
        session['username']     = username
        session['display_name'] = users[username].get('display_name', name)
        return jsonify({'success': True})
    except urllib.error.URLError:
        return jsonify({'error': 'Could not verify with Google — check your internet'}), 503
    except Exception as e:
        return jsonify({'error': f'Google sign-in failed: {str(e)}'}), 401

@app.route('/api/login', methods=['POST'])
def do_login():
    data     = request.json
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'Fill in both fields'}), 400
    users = load_users()
    if username not in users:
        return jsonify({'error': 'No account found — sign up first'}), 401
    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Wrong password'}), 401
    session['username']     = username
    session['display_name'] = users[username].get('display_name', username)
    return jsonify({'success': True})

@app.route('/api/register', methods=['POST'])
def do_register():
    data         = request.json
    username     = data.get('username', '').strip().lower()
    password     = data.get('password', '')
    display_name = data.get('display_name', '').strip() or username
    if not username or not password:
        return jsonify({'error': 'Fill in all fields'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    users = load_users()
    if username in users:
        return jsonify({'error': 'Username already taken — try another'}), 409
    users[username] = {
        'password':     generate_password_hash(password),
        'display_name': display_name,
    }
    save_users(users)
    session['username']     = username
    session['display_name'] = display_name
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ── Main app ────────────────────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    return render_template('index.html', styles=STYLES, color_hex=COLOR_HEX,
                           color_seasons=COLOR_SEASONS, body_types=BODY_TYPES,
                           display_name=session.get('display_name',''))

@app.route('/api/wardrobe', methods=['GET'])
def get_wardrobe(): return jsonify(load_wardrobe())

@app.route('/api/wardrobe', methods=['POST'])
def add_item():
    item = request.json
    items = load_wardrobe()
    item['id'] = f"item_{len(items)+1}_{item['name'].lower().replace(' ','_')}"
    item['is_clean'] = True
    items.append(item)
    save_wardrobe(items)
    return jsonify({'success': True, 'item': item})

@app.route('/api/wardrobe/<item_id>', methods=['DELETE'])
def del_item(item_id):
    save_wardrobe([i for i in load_wardrobe() if i['id'] != item_id])
    return jsonify({'success': True})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data  = request.json
    items = load_wardrobe()
    if not items: return jsonify({'outfits': [], 'empty': True})
    engine = RecommendationEngine(to_engine(items))
    try:
        results = engine.recommend(int(data.get('temp',22)), Occasion(data.get('occasion','casual')), bool(data.get('rain',False)), top_n=3)
        outfits = []
        for o in results:
            outfit = {'score': o.score, 'items': []}
            for role, itm in [('Top/Dress',o.top),('Bottom',o.bottom),('Outerwear',o.outerwear),('Shoes',o.shoes)]:
                if itm: outfit['items'].append({'role':role,'name':itm.name,'color':itm.color,'hex':COLOR_HEX.get(itm.color.lower(),'#888888')})
            outfits.append(outfit)
        return jsonify({'outfits': outfits})
    except Exception as e:
        return jsonify({'outfits': [], 'error': str(e)})

@app.route('/api/outfit-verdict', methods=['POST'])
def outfit_verdict():
    data  = request.json
    items = data.get('items', [])   # [{ name, color, category }]
    style = data.get('style', 'minimalist')
    color_season = data.get('color_season', '')
    body_type    = data.get('body_type', '')

    rule_result = compute_verdict(items)

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if ANTHROPIC_AVAILABLE and api_key and items:
        cs_hint = f" The user's color season is {COLOR_SEASONS[color_season]['name']} — best colors: {', '.join(COLOR_SEASONS[color_season]['best_colors'][:4])}." if color_season in COLOR_SEASONS else ""
        bt_hint = f" Their body type is {BODY_TYPES[body_type]['name']} — goal: {BODY_TYPES[body_type]['goal']}." if body_type in BODY_TYPES else ""
        item_list = "\n".join(f"- {i['name']} ({i['color']} {i['category']})" for i in items)
        prompt = f"""A user has built this outfit:\n{item_list}\nTheir style: {STYLES.get(style,{}).get('name','')}.{cs_hint}{bt_hint}\n\nGive a verdict in 3-4 sentences: rate the color harmony, note what works, suggest one improvement. Be specific and stylish."""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            resp   = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=250,
                       messages=[{"role":"user","content":prompt}])
            rule_result['ai_verdict'] = resp.content[0].text
        except Exception: pass

    return jsonify(rule_result)

@app.route('/api/chat', methods=['POST'])
def chat():
    data    = request.json
    msg     = data.get('message', '')
    style   = data.get('style', 'minimalist')
    history = data.get('history', [])
    csea    = data.get('color_season', '')
    btype   = data.get('body_type', '')
    items   = load_wardrobe()
    p       = STYLES.get(style, STYLES['minimalist'])
    wsum    = "\n".join(f"- {i['name']} ({i['color']} {i['category']})" for i in items) or "No items yet."

    cs_ctx = f"\nUser's color season: {COLOR_SEASONS[csea]['name']} — best colors: {', '.join(COLOR_SEASONS[csea]['best_colors'][:4])}. Avoid: {', '.join(COLOR_SEASONS[csea]['avoid'][:2])}." if csea in COLOR_SEASONS else ""
    bt_ctx = f"\nUser's body type: {BODY_TYPES[btype]['name']} — goal: {BODY_TYPES[btype]['goal']}. Best cuts: {', '.join(BODY_TYPES[btype]['best_cuts'][:3])}." if btype in BODY_TYPES else ""

    tone_map = {'kawaii':'bubbly, enthusiastic, use 🎀 and cute words','emo':'poetic and a little dramatic, dark humor, use 🖤','minimalist':'calm and precise, no fluff, short sharp sentences','streetwear':'casual and cool, hype energy, use 🔥 and 🧢','cottagecore':'gentle and dreamy, nature metaphors, use 🌿 and 🌸','y2k':'enthusiastic bestie energy, nostalgic, use ✨','gyaru':'confident and glamorous, use 💅','formal':'professional and direct, authoritative'}

    system_prompt = f"""You are Vouge — a witty, knowledgeable AI fashion stylist inside the vougeabulary app. You have a real personality and can hold genuine conversations about anything, but you always bring it back to fashion, style, and helping the user look amazing.

Current style aesthetic: {p['name']} ({p['tagline']}) — {p['description']}
Style keywords: {', '.join(p['keywords'])}
Recommended brands: {', '.join(p['brands'])}{cs_ctx}{bt_ctx}

The user's wardrobe:
{wsum}

Your personality tone: {tone_map.get(style, 'friendly and helpful')}

Rules:
- Have real conversations — respond naturally to greetings, feelings, small talk, then steer toward fashion
- When suggesting outfits, always reference specific items from the user's wardrobe above
- For shopping, include clickable links like [Shop on ASOS](https://www.asos.com/search/?q=query) or [Search Google](https://www.google.com/search?q=query)
- Factor in the user's color season and body type when giving advice
- Keep replies conversational — 2 to 4 sentences, never robotic or listy unless asked
- Never say "As an AI" or break character"""

    messages_to_send = (history or [])[-12:] + [{"role": "user", "content": msg}]

    # Try Groq first (free)
    groq_key = os.environ.get('GROQ_API_KEY', '')
    if GROQ_AVAILABLE and groq_key:
        try:
            client = GroqClient(api_key=groq_key)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + messages_to_send,
                max_tokens=400,
                temperature=0.85,
            )
            return jsonify({'response': resp.choices[0].message.content, 'powered_by': 'Vouge AI'})
        except Exception:
            pass

    # Try Anthropic second
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if ANTHROPIC_AVAILABLE and anthropic_key:
        try:
            client = anthropic.Anthropic(api_key=anthropic_key)
            resp   = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=400,
                       system=system_prompt, messages=messages_to_send)
            return jsonify({'response': resp.content[0].text, 'powered_by': 'Vouge AI'})
        except Exception:
            pass

    # Rule-based fallback
    return jsonify({'response': rule_chat(msg, style, items, csea, btype), 'powered_by': 'Vouge AI'})

@app.route('/api/shop/<style>')
def shop(style):
    p = STYLES.get(style, STYLES['minimalist'])
    links = [{'term':t,'google':f"https://www.google.com/search?q={t.replace(' ','+')}",
              'asos':f"https://www.asos.com/search/?q={t.replace(' ','+')}",
              'pinterest':f"https://www.pinterest.com/search/pins/?q={t.replace(' ','+')}",
              'depop':f"https://www.depop.com/search/?q={t.replace(' ','+')}"}
             for t in p['searches']]
    return jsonify({**p, 'links': links})

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Accept a base64 image and save it to static/uploads/. Returns the URL path."""
    data     = request.json
    img_data = data.get('image', '')          # data:image/...;base64,...
    item_id  = data.get('item_id', 'unknown')
    if not img_data:
        return jsonify({'error': 'No image provided'}), 400
    # Strip the data URI prefix
    if ',' in img_data:
        header, encoded = img_data.split(',', 1)
        ext = header.split('/')[1].split(';')[0]   # e.g. "jpeg"
    else:
        encoded, ext = img_data, 'jpg'
    uploads_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    filename = f"{item_id}.{ext}"
    filepath = os.path.join(uploads_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(encoded))
    # Save image path on the wardrobe item
    items = load_wardrobe()
    for i in items:
        if i['id'] == item_id:
            i['image'] = f"/static/uploads/{filename}"
            break
    save_wardrobe(items)
    return jsonify({'success': True, 'url': f"/static/uploads/{filename}"})

@app.route('/api/color-seasons')
def get_color_seasons(): return jsonify(COLOR_SEASONS)

@app.route('/api/body-types')
def get_body_types(): return jsonify(BODY_TYPES)

# ── Clean / dirty toggle ───────────────────────────────────────────────────────
@app.route('/api/wardrobe/<item_id>/toggle-clean', methods=['PATCH'])
def toggle_clean(item_id):
    items = load_wardrobe()
    for i in items:
        if i['id'] == item_id:
            i['is_clean'] = not i.get('is_clean', True)
            save_wardrobe(items)
            return jsonify({'success': True, 'is_clean': i['is_clean']})
    return jsonify({'error': 'Not found'}), 404

# ── Saved outfits ──────────────────────────────────────────────────────────────
@app.route('/api/saved-outfits', methods=['GET'])
def get_saved_outfits():
    return jsonify(load_saved_fits())

@app.route('/api/saved-outfits', methods=['POST'])
def save_outfit():
    data  = request.json
    fits  = load_saved_fits()
    fit   = {
        'id':        f"fit_{len(fits)+1}_{random.randint(1000,9999)}",
        'score':     data.get('score', 0),
        'items':     data.get('items', []),
        'occasion':  data.get('occasion', ''),
        'style':     data.get('style', ''),
        'saved_at':  __import__('datetime').datetime.now().strftime('%b %d, %Y'),
    }
    fits.append(fit)
    save_saved_fits(fits)
    return jsonify({'success': True, 'fit': fit})

@app.route('/api/saved-outfits/<fit_id>', methods=['DELETE'])
def delete_saved_outfit(fit_id):
    save_saved_fits([f for f in load_saved_fits() if f['id'] != fit_id])
    return jsonify({'success': True})

# ── Capsule wardrobe analysis ──────────────────────────────────────────────────
@app.route('/api/capsule-analysis', methods=['GET'])
def capsule_analysis():
    items = load_wardrobe()
    if not items:
        return jsonify({'error': 'Wardrobe is empty'})

    cats = {}
    for i in items:
        cats.setdefault(i['category'], []).append(i)

    tops     = cats.get('top', []) + cats.get('dress', [])
    bottoms  = cats.get('bottom', [])
    shoes    = cats.get('shoes', [])
    outer    = cats.get('outerwear', [])
    acc      = cats.get('accessory', [])

    # Count valid outfit combos (top+bottom, or dress alone) × shoes options
    base_combos = len(tops) * len(bottoms) + len(cats.get('dress', []))
    combos_with_shoes = base_combos * max(len(shoes), 1)

    # Color variety score
    colors = list({i['color'].lower() for i in items})
    neutral_colors = {'white','black','grey','gray','beige','navy','cream','camel','charcoal','tan'}
    neutrals_count = sum(1 for c in colors if c in neutral_colors)
    color_score = min(100, round((neutrals_count / max(len(colors),1)) * 50 + min(len(colors),10) * 5))

    # Gap analysis
    gaps = []
    if not tops:       gaps.append(('tops',        'You have no tops — add some to unlock outfits'))
    if not bottoms:    gaps.append(('bottoms',      'No bottoms detected — trousers or skirts needed'))
    if not shoes:      gaps.append(('shoes',        'No shoes in wardrobe — recommendations ignore footwear'))
    if not outer:      gaps.append(('outerwear',    'No outerwear — add a jacket or coat for cold/rainy days'))
    if len(tops) < 3:  gaps.append(('more tops',    f'Only {len(tops)} top(s) — 5+ unlocks far more combos'))
    if neutrals_count < 2: gaps.append(('neutrals', 'Add white, black, or beige basics — they pair with everything'))

    # Potential if gaps filled
    projected = (max(len(tops),3) * max(len(bottoms),2)) * max(len(shoes),2)

    dirty_count = sum(1 for i in items if not i.get('is_clean', True))

    return jsonify({
        'total_items':      len(items),
        'outfit_combos':    combos_with_shoes,
        'projected_combos': projected,
        'color_variety':    len(colors),
        'neutrals_count':   neutrals_count,
        'dirty_count':      dirty_count,
        'category_counts':  {k: len(v) for k, v in cats.items()},
        'gaps':             gaps,
        'color_score':      color_score,
        'colors_list':      colors[:12],
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
