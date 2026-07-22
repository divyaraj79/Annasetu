from app.automation.groq_client import GroqClient


client = GroqClient()

email = """
Food Name: Veg Biryani
Food Category: Cooked Meal
Quantity: 40
Quantity Unit: Plates
Vegetarian: Yes
Cooked At: 1:30 PM
Pickup Address: ABC Restaurant, Ahmedabad
Special Notes: Please collect before 8 PM.
"""

response = client.extract_donation(email)

print(type(response))
print(response)