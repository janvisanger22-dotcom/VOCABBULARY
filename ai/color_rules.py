# Color compatibility rules for outfit matching.
# Colors are grouped by tone family; compatibility is determined by group relationships.

COLOR_GROUPS: dict[str, list[str]] = {
    "neutral": ["black", "white", "grey", "gray", "beige", "cream", "navy", "camel", "ivory"],
    "warm":    ["red", "orange", "yellow", "pink", "coral", "burgundy", "maroon", "peach"],
    "cool":    ["blue", "green", "purple", "teal", "mint", "lavender", "cyan", "indigo"],
    "earth":   ["brown", "olive", "mustard", "rust", "tan", "khaki", "sand"],
}

# Pairwise compatibility scores (0.0 = clash, 1.0 = perfect match)
_COMPATIBILITY: dict[tuple[str, str], float] = {
    ("neutral", "neutral"): 1.0,
    ("neutral", "warm"):    1.0,
    ("neutral", "cool"):    1.0,
    ("neutral", "earth"):   1.0,
    ("warm",    "warm"):    0.8,   # monochromatic / analogous
    ("cool",    "cool"):    0.8,
    ("earth",   "earth"):   0.85,
    ("warm",    "earth"):   0.75,
    ("cool",    "earth"):   0.7,
    ("warm",    "cool"):    0.4,   # tends to clash
}


def get_color_group(color: str) -> str:
    color = color.lower().strip()
    for group, members in COLOR_GROUPS.items():
        if color in members:
            return group
    return "neutral"  # unknown colors treated as neutral


def color_compatibility_score(color_a: str, color_b: str) -> float:
    """Return a 0.0–1.0 score for how well two colors pair together."""
    g1 = get_color_group(color_a)
    g2 = get_color_group(color_b)
    key = (g1, g2) if (g1, g2) in _COMPATIBILITY else (g2, g1)
    return _COMPATIBILITY.get(key, 0.5)
