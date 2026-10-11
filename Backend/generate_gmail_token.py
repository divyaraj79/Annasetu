from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    SCOPES,
)

credentials = flow.run_local_server(
    port=0,
    access_type="offline",
    prompt="consent",
)

with open("token.json", "w", encoding="utf-8") as token_file:
    token_file.write(credentials.to_json())

print("Gmail token generated successfully.")
print("Saved to token.json")
print("Refresh token available:", bool(credentials.refresh_token))