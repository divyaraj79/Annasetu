from app.models.donation import Donation
from app.models.match import Match
from app.models.ngo import NGO


# --------------------------------------------------
# Email Subjects
# --------------------------------------------------

DONATION_UPDATE = "Donation Update"

DONATION_CANCELLED = "Donation Cancellation"

DONATION_ACCEPTED = (
    "Donation Accepted"
)

DONATION_EMAIL = "Food Donation"

DONATION_UNMATCHED = "Donation Unmatched"

NGO_NOTIFICATION = "Food Donation Opportunity"

RESTAURANT_REGISTRATION_APPROVED = "Restaurant Registration Approved"

NGO_REGISTRATION_APPROVED = (
    "NGO Registration Approved"
)

MATCH_TIMEOUT = "Donation Response Timeout"

DONATION_VALIDATION_FAILED = (
    "Donation Could Not Be Processed"
)

NEED_EMAIL = "Food Need"


# --------------------------------------------------
# Templates
# --------------------------------------------------

def registration_approved_template() -> str:

    return """
        Hello,

        Congratulations!

        Your restaurant has been approved on AnnaSetu.

        You can now donate surplus food simply by sending an email.

        Subject:
        Food Donation

        Please include at least the following details:
            • Donation Title
            • Donation Items
            • Food Category
            • Vegetarian / Non-Vegetarian
            • Cooked Time
            • Expiry Time
            • Pickup Address
            • Special Notes (Optional)

        Example:

            Donation Title:
            Mixed Vegetarian Meal

            Donation Items:
            Veg Biryani - 20 kg
            Dal Tadka - 15 kg
            Jeera Rice - 18 kg
            Raita - 12 liters

            Food Category:
            main_course

            Vegetarian:
            Yes

            Cooked At:
            24 July 2026 8:30 PM

            Expiry Time:
            25 July 2026 7:00 AM

            Pickup Address:
            ABC Restaurant, Ahmedabad

            Special Notes:
            Please collect before 1 AM.

        Examples of Food Category:
            main_course
            snacks
            dessert
            beverage
            bakery
            other


        You may either follow the above format
        or write naturally in plain English.

        AnnaSetu AI will automatically extract
        the required information.

        Providing the information clearly
        improves extraction accuracy.

        Note:
            Our AI reads your emails automatically.
            Providing the above information clearly will improve processing accuracy.

        Thank you for helping reduce food waste.

        Team AnnaSetu
        """


def ngo_notification_template(
    donation: Donation,
    match: Match,
) -> str:

    return f"""
        Hello,

        A food donation matching your
        current needs is available.

        Reference ID (Do not remove this when replying):
        {match.id}

        Donation Title:
        {donation.food_name}

        Category:
        {donation.food_category.value}

        Quantity:
        {donation.quantity} {donation.quantity_unit.value}

        Vegetarian:
        {"Yes" if donation.is_vegetarian else "No"}

        Pickup Address:
        {donation.pickup_address}

        Food Expiry:
        {donation.expiry_time}

        Please reply within 30 minutes.

        Simply reply to this email.

        Reply using one of the following formats.

        ----------------------------------------

        Accept

        Reference ID:
        {match.id}

        ----------------------------------------

        Decline

        Reason:
        No volunteers available today.

        Reference ID:
        {match.id}

        ----------------------------------------

        Donation Received

        Reference ID:
        {match.id}

        ----------------------------------------

        Please keep the Reference ID exactly as provided.

        Thank you.

        Team AnnaSetu
        """


def donation_accepted_template(
    ngo: NGO,
) -> str:

    return f"""
        Hello,

        Your donation has been accepted.

        NGO:
        {ngo.ngo_name}

        The NGO will contact you shortly
        for pickup.

        Thank you for donating through
        AnnaSetu.
        """


def donation_unmatched_template() -> str:

    return """
        Hello,

        Unfortunately,
        no NGO was able to accept
        your donation.

        The donation has been marked
        as unmatched.

        Thank you for supporting
        AnnaSetu.
        """


def match_timeout_template() -> str:

    return """
        Hello,

        The response window for this
        donation has expired.

        The donation opportunity has
        been reassigned.

        Thank you.

        Team AnnaSetu
        """

def ngo_registration_approved_template() -> str:

    return """
        Hello,

        Congratulations!

        Your NGO has been approved on AnnaSetu.

        You will now receive food donation
        requests through this email address.

        Each donation email contains:
            • Reference ID
            • Donation Title
            • Food Category
            • Number of Donation Items
            • Pickup Address
            • Expiry Time

        To ACCEPT a donation:

        Simply reply to the same email.

        To ACCEPT a donation:

        Accept

        Reference ID:
        <Reference ID>

        ----------------------------------------

        To DECLINE a donation:

        Decline

        Reason:
        No volunteers available today.

        Reference ID:
        <Reference ID>

        ----------------------------------------

        After successfully collecting the donation:
            Donation Received

        Reference ID:
        <Reference ID>

        ----------------------------------------

        Always copy the Reference ID exactly as provided in the donation email.

        Important:

        • Reply using this registered email address.
        • Do not change the email subject.
        • Keep the Reference ID in the email thread.
        • Reply within 30 minutes.

        Our AI automatically understands
        your reply.

        Thank you for helping reduce food waste.

        Team AnnaSetu
        """


def donation_validation_failed_template(
    reason: str,
) -> str:

    return f"""
        Hello,

        We received your Food Donation email
        but could not process it.

        Reason:

        {reason}

        Please correct the above issue and
        send a NEW email with the subject:

        Food Donation

        You do not need to reply to the
        previous email.

        Thank you for supporting AnnaSetu.

        Team AnnaSetu
        """