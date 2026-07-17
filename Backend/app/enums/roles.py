from enum import Enum


class UserRole(str, Enum):
    RESTAURANT = "restaurant"
    NGO = "ngo"
    ADMIN = "admin"