"""
Database Layer — vougeabulary
Lead: Tanish (Backend — Database & Integration)

Handles all read/write operations for wardrobe data.
Currently uses JSON flat-file storage (prototype).
To upgrade to MongoDB, replace the functions below with
pymongo queries — no other file needs to change.
"""
import json
import os

DATA_DIR      = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
WARDROBE_FILE = os.path.join(DATA_DIR, 'wardrobe.json')

# ── Valid field values ────────────────────────────────────────────────────────

VALID_CATEGORIES = {'top', 'bottom', 'dress', 'outerwear', 'shoes', 'accessory'}
VALID_OCCASIONS  = {'casual', 'work', 'formal', 'party', 'sport'}
VALID_WEATHER    = {'hot', 'warm', 'cool', 'cold', 'rainy'}


# ── Schema ────────────────────────────────────────────────────────────────────

"""
ClothingItem schema:
{
    "id":        string  — unique, auto-generated
    "name":      string  — display name
    "category":  string  — one of VALID_CATEGORIES
    "color":     string  — lowercase color name
    "occasions": list    — subset of VALID_OCCASIONS (at least 1)
    "weather":   list    — subset of VALID_WEATHER   (at least 1)
    "is_clean":  boolean — availability flag (default true)
}
"""


# ── CRUD Operations ───────────────────────────────────────────────────────────

def get_all_items() -> list[dict]:
    """Load and return all wardrobe items from disk."""
    if not os.path.exists(WARDROBE_FILE):
        return []
    with open(WARDROBE_FILE, encoding='utf-8') as f:
        return json.load(f)


def add_item(item: dict) -> dict:
    """
    Validate, assign an ID, and persist a new clothing item.
    Returns the saved item (with generated ID).
    Raises ValueError if validation fails.
    """
    _validate(item)
    items       = get_all_items()
    item['id']  = _generate_id(item['name'], len(items))
    item['color']     = item['color'].lower().strip()
    item['is_clean']  = item.get('is_clean', True)
    items.append(item)
    _save(items)
    return item


def delete_item(item_id: str) -> bool:
    """
    Remove item by ID. Returns True if item existed, False if not found.
    """
    items    = get_all_items()
    filtered = [i for i in items if i['id'] != item_id]
    found    = len(filtered) < len(items)
    _save(filtered)
    return found


def mark_dirty(item_id: str) -> bool:
    """Mark a clothing item as not clean (e.g. it has been worn)."""
    items = get_all_items()
    for i in items:
        if i['id'] == item_id:
            i['is_clean'] = False
            _save(items)
            return True
    return False


def mark_clean(item_id: str) -> bool:
    """Mark a clothing item as clean (e.g. after washing)."""
    items = get_all_items()
    for i in items:
        if i['id'] == item_id:
            i['is_clean'] = True
            _save(items)
            return True
    return False


def get_by_category(category: str) -> list[dict]:
    """Return all clean items of a specific category."""
    return [i for i in get_all_items()
            if i.get('category') == category and i.get('is_clean', True)]


def get_summary() -> dict:
    """Return a summary count of the wardrobe by category."""
    items   = get_all_items()
    summary = {cat: 0 for cat in VALID_CATEGORIES}
    for i in items:
        cat = i.get('category', '')
        if cat in summary:
            summary[cat] += 1
    summary['total'] = len(items)
    return summary


# ── Private helpers ───────────────────────────────────────────────────────────

def _generate_id(name: str, count: int) -> str:
    slug = name.lower().strip().replace(' ', '_')
    return f"item_{count + 1}_{slug}"


def _save(items: list[dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(WARDROBE_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)


def _validate(item: dict) -> None:
    errors = []
    if not item.get('name', '').strip():
        errors.append("name is required")
    if item.get('category') not in VALID_CATEGORIES:
        errors.append(f"category must be one of {VALID_CATEGORIES}")
    if not item.get('color', '').strip():
        errors.append("color is required")
    bad_occ = set(item.get('occasions', [])) - VALID_OCCASIONS
    if bad_occ or not item.get('occasions'):
        errors.append(f"occasions must be non-empty subset of {VALID_OCCASIONS}")
    bad_wth = set(item.get('weather', [])) - VALID_WEATHER
    if bad_wth or not item.get('weather'):
        errors.append(f"weather must be non-empty subset of {VALID_WEATHER}")
    if errors:
        raise ValueError("Validation failed: " + "; ".join(errors))
