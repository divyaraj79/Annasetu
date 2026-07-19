from enum import Enum


class QuantityUnit(str, Enum):
    KG = "kg"
    LITERS = "liters"
    PIECE = "piece"