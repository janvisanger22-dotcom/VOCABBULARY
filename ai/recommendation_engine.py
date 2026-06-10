from typing import List, Optional
from clothing_item import ClothingItem, Category, Occasion, Outfit, Weather, Wardrobe
from color_rules import color_compatibility_score


def weather_from_input(temp_celsius: int, is_raining: bool = False) -> Weather:
    """Convert temperature and rain flag into a Weather enum value."""
    if is_raining:
        return Weather.RAINY
    if temp_celsius >= 30:
        return Weather.HOT
    if temp_celsius >= 20:
        return Weather.WARM
    if temp_celsius >= 10:
        return Weather.COOL
    return Weather.COLD


def _filter(items: List[ClothingItem], weather: Weather, occasion: Occasion) -> List[ClothingItem]:
    return [
        i for i in items
        if weather in i.weather_suitability and occasion in i.occasions
    ]


def _score_outfit(top: ClothingItem, bottom: Optional[ClothingItem],
                  shoes: Optional[ClothingItem]) -> float:
    """
    Score an outfit 0–100 based on color harmony.
    Weights: top-bottom pair (50pts), top-shoes (25pts), bottom-shoes (25pts).
    """
    score = 0.0
    if bottom:
        score += color_compatibility_score(top.color, bottom.color) * 50
    else:
        score += 50  # dress (no separate bottom) gets full top-bottom points
    if shoes:
        ref_color = bottom.color if bottom else top.color
        score += color_compatibility_score(top.color, shoes.color) * 25
        score += color_compatibility_score(ref_color, shoes.color) * 25
    return round(score, 1)


class RecommendationEngine:
    def __init__(self, wardrobe: Wardrobe):
        self.wardrobe = wardrobe

    def recommend(
        self,
        temp_celsius: int,
        occasion: Occasion,
        is_raining: bool = False,
        top_n: int = 3,
    ) -> List[Outfit]:
        """
        Generate ranked outfit recommendations.

        Steps:
          1. Convert weather input to a Weather category.
          2. Filter each clothing category by weather + occasion.
          3. Build every valid top+bottom (or dress) combination.
          4. For each combination, pick the best-scoring shoes.
          5. Attach outerwear when the weather demands it.
          6. Return the top_n highest-scoring outfits.
        """
        weather = weather_from_input(temp_celsius, is_raining)

        tops      = _filter(self.wardrobe.get_by_category(Category.TOP),       weather, occasion)
        bottoms   = _filter(self.wardrobe.get_by_category(Category.BOTTOM),    weather, occasion)
        dresses   = _filter(self.wardrobe.get_by_category(Category.DRESS),     weather, occasion)
        shoes_all = _filter(self.wardrobe.get_by_category(Category.SHOES),     weather, occasion)
        outers    = _filter(self.wardrobe.get_by_category(Category.OUTERWEAR), weather, occasion)

        outfits: List[Outfit] = []

        # --- top + bottom combinations ---
        for top in tops:
            for bottom in bottoms:
                best_shoe = self._best_shoe(shoes_all, top.color, bottom.color)
                score = _score_outfit(top, bottom, best_shoe)
                outfits.append(Outfit(top=top, bottom=bottom, shoes=best_shoe, score=score))

        # --- dress combinations (no separate bottom) ---
        for dress in dresses:
            best_shoe = self._best_shoe(shoes_all, dress.color, dress.color)
            score = _score_outfit(dress, None, best_shoe)
            outfits.append(Outfit(top=dress, bottom=None, shoes=best_shoe, score=score))

        # Sort best first
        outfits.sort(key=lambda o: o.score, reverse=True)
        top_outfits = outfits[:top_n]

        # Attach outerwear for cold / cool / rainy weather
        needs_outer = weather in {Weather.COLD, Weather.COOL, Weather.RAINY}
        if needs_outer and outers:
            for outfit in top_outfits:
                ref = outfit.top.color if outfit.top else "black"
                outfit.outerwear = max(outers, key=lambda o: color_compatibility_score(ref, o.color))

        return top_outfits

    @staticmethod
    def _best_shoe(
        shoes: List[ClothingItem], top_color: str, bottom_color: str
    ) -> Optional[ClothingItem]:
        if not shoes:
            return None
        return max(
            shoes,
            key=lambda s: (
                color_compatibility_score(top_color, s.color)
                + color_compatibility_score(bottom_color, s.color)
            ),
        )
