from enum import Enum


class FoodCategory(str, Enum):
    MAIN_COURSE = "main_course"
    SNACKS = "snacks"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    BAKERY = "bakery"
    OTHER = "other"