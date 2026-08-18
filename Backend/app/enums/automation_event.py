from enum import Enum


class AutomationEvent(str, Enum):
    DONATION_CREATED = "donation_created"
    NEED_CREATED = "need_created"

    NGO_ACCEPTED = "ngo_accepted"
    NGO_DECLINED = "ngo_declined"

    MATCH_TIMEOUT = "match_timeout"

    DONATION_EXPIRED = "donation_expired"