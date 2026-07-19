from enum import Enum


class DonationStatus(str, Enum):
    CREATED = "created"
    MATCHING = "matching"
    PENDING = "pending"
    ACCEPTED = "accepted"
    # PICKED_UP = "picked_up"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class MatchStatus(str, Enum):
    PENDING = "pending"
    INTERESTED = "interested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    # TIMEOUT = "timeout"