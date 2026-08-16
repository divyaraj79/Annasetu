from enum import Enum
class DonationStatus(str, Enum):
    UNMATCHED = "unmatched"
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
    NOTIFIED = "notified"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    REJECTED = "rejected"
    COMPLETED = "completed"
    # TIMEOUT = "timeout"