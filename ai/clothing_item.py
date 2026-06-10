from dataclasses import dataclass, field
from typing import List
from enum import Enum


class Category(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    DRESS = "dress"
    OUTERWEAR = "outerwear"
    SHOES = "shoes"
    ACCESSORY = "accessory"


class Occasion(Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    WORK = "work"
    SPORT = "sport"
    PARTY = "party"


class Weather(Enum):
    HOT = "hot"        # 30°C and above
    WARM = "warm"      # 20–29°C
    COOL = "cool"      # 10–19°C
    COLD = "cold"      # below 10°C
    RAINY = "rainy"


@dataclass
class ClothingItem:
    item_id: str
    name: str
    category: Category
    color: str
    occasions: List[Occasion]
    weather_suitability: List[Weather]
    is_clean: bool = True

    def __repr__(self):
        return f"{self.name} ({self.color}, {self.category.value})"


@dataclass
class Outfit:
    top: ClothingItem | None
    bottom: ClothingItem | None
    shoes: ClothingItem | None
    outerwear: ClothingItem | None = None
    score: float = 0.0

    def display(self):
        parts = []
        if self.top:
            parts.append(f"  Top      : {self.top}")
        if self.bottom:
            parts.append(f"  Bottom   : {self.bottom}")
        if self.outerwear:
            parts.append(f"  Outerwear: {self.outerwear}")
        if self.shoes:
            parts.append(f"  Shoes    : {self.shoes}")
        parts.append(f"  Score    : {self.score:.0f}/100")
        return "\n".join(parts)


class Wardrobe:
    def __init__(self):
        self.items: List[ClothingItem] = []

    def add_item(self, item: ClothingItem):
        self.items.append(item)

    def get_by_category(self, category: Category) -> List[ClothingItem]:
        return [i for i in self.items if i.category == category and i.is_clean]

    def summary(self):
        print(f"Wardrobe has {len(self.items)} items:")
        for item in self.items:
            print(f"  - {item}")
