from enum import Enum


class QuantityUnit(str, Enum):
    MEALS = "meals"
    PLATES = "plates"
    KG = "kg"
    LITERS = "liters"
    PACKETS = "packets"
    OTHER = "other"