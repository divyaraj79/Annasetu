from app.automation.email_client import EmailClient

client = EmailClient()

client.authenticate()

messages = client.fetch_unread_messages(
    max_results=1
)

if messages:

    email = client.get_message(
        messages[0]["id"]
    )

    print(email)

else:

    print("No unread emails.")