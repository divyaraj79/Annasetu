from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

import base64
from email.header import decode_header
from email.mime.text import MIMEText


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]


class EmailClient:

    def __init__(self):

        self.credentials_path = (
            Path("credentials.json")
        )

        self.token_path = (
            Path("token.json")
        )

        self.service = None


    def _get_service(self):

        if self.service is None:
            self.authenticate()

        return self.service
    

    def authenticate(self):
        """
        Authenticate with Gmail API.

        Creates token.json on first login
        and refreshes expired tokens
        automatically.
        """

        credentials = None

        if self.token_path.exists():

            credentials = Credentials.from_authorized_user_file(
                self.token_path,
                SCOPES,
            )

        if (
            credentials is None
            or not credentials.valid
        ):

            if (
                credentials
                and credentials.expired
                and credentials.refresh_token
            ):

                credentials.refresh(
                    Request()
                )

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path,
                    SCOPES,
                )

                credentials = flow.run_local_server(
                    port=0
                )

            self.token_path.write_text(
                credentials.to_json()
            )

        self.service = build(
            "gmail",
            "v1",
            credentials=credentials,
        )

        return self.service


    def fetch_unread_messages(
        self,
        max_results: int = 10,
    ) -> list[dict]:
        """
        Fetch unread messages from Gmail.

        Returns a list containing
        Gmail message metadata.
        """

        service = self._get_service()

        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q="in:inbox is:unread",
                maxResults=max_results,
            )
            .execute()
        )

        messages = []

        for message in response.get(
            "messages",
            [],
        ):

            messages.append(
                self.get_message(
                    message["id"]
                )
            )

        return messages
    
    def _extract_body(
        self,
        payload: dict,
    ) -> str:
        """
        Extract plain text body
        from a Gmail message.
        """

        body = ""

        if "parts" in payload:

            for part in payload["parts"]:

                if part.get("mimeType") == "text/plain":

                    data = (
                        part["body"]
                        .get("data")
                    )

                    if data:

                        body = base64.urlsafe_b64decode(
                            data
                        ).decode()

                        break

        else:

            data = (
                payload["body"]
                .get("data")
            )

            if data:

                body = base64.urlsafe_b64decode(
                    data
                ).decode()

        return body


    def get_message(
        self,
        message_id: str,
    ) -> dict:
        """
        Fetch a complete Gmail message.

        Returns:
            id
            thread_id
            subject
            sender
            recipient
            date
            body
        """

        service = self._get_service()

        message = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )

        headers = message["payload"].get(
            "headers",
            []
        )

        subject = ""
        sender = ""
        recipient = ""
        date = ""

        for header in headers:

            name = header["name"].lower()

            if name == "subject":
                decoded = decode_header(
                    header["value"]
                )

                subject = "".join(
                    part.decode(encoding or "utf-8")
                    if isinstance(part, bytes)
                    else part
                    for part, encoding in decoded
                )

            elif name == "from":
                sender = header["value"]

            elif name == "to":
                recipient = header["value"]

            elif name == "date":
                date = header["value"]

        body = self._extract_body(
            message["payload"]
        )

        return {
            "id": message["id"],
            "thread_id": message["threadId"],
            "subject": subject,
            "from": sender,
            "to": recipient,
            "date": date,
            "body": body,
        }
    

    def mark_as_read(
        self,
        message_id: str,
    ) -> None:
        """
        Mark a Gmail message as read.
        """

        service = self._get_service()

        (
            service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={
                    "removeLabelIds": [
                        "UNREAD",
                    ],
                },
            )
            .execute()
        )

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> dict:
        """
        Send an email using Gmail.
        """

        service = self._get_service()

        message = MIMEText(body)

        message["to"] = recipient
        message["subject"] = subject

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        return (
            service.users()
            .messages()
            .send(
                userId="me",
                body={
                    "raw": encoded_message,
                },
            )
            .execute()
        )