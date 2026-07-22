from app.models.donation import Donation
from app.models.match import Match
from app.models.ngo import NGO


# --------------------------------------------------
# Email Subjects
# --------------------------------------------------

DONATION = "Food Donation"

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

        • Food Name
        • Food Category
        • Quantity
        • Quantity Unit
        • Vegetarian / Non-Vegetarian
        • Cooked Time
        • Pickup Address
        • Special Notes (Optional)

        Example: 
            Food Name: Veg Biryani
            Food Category: main_course
            Quantity: 40
            Quantity Unit: kg
            Vegetarian: Yes
            Cooked At: 1:30 PM
            Pickup Address: ABC Restaurant, Ahmedabad
            Special Notes: Please collect before 8 PM.

        Examples of Food Category:
            main_course
            snacks
            dessert
            beverage
            bakery
            other

        Examples of Quantity Unit:
            kg
            liters
            piece

        You may also write naturally.
        AnnaSetu will automatically extract
        the required information.

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

        Food Name:
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

        Examples:

        Examples:
            Accept

            or

            Decline:
            No volunteers available today.

        Decline:
        "Sorry, we don't have volunteers today."

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
        • Food Details
        • Quantity
        • Pickup Address
        • Expiry Time

        To ACCEPT a donation:

        Simply reply to the same email.

        Example:

        Accept

        To DECLINE a donation:

        Reply with:

        Decline:
        No volunteers available today.

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