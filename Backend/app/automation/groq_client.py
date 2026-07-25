import os
import json

from dotenv import load_dotenv

from groq import Groq

from app.automation.prompts.groq_prompts import (
    DONATION_EXTRACTION_PROMPT,
    NGO_REPLY_PROMPT,
    NEED_EXTRACTION_PROMPT,
)


load_dotenv()


class GroqClient:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)
            cls._instance.client = None
            cls._instance.model = None

        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        if self.client is not None:
            return

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables."
            )

        self.client = Groq(
            api_key=api_key,
        )

        self.model = "llama-3.3-70b-versatile"

        self._initialized = True

    def _chat(
        self,
        prompt: str,
        message: str,
        temperature: float = 0,
    ) -> str:
        """
        Send a chat completion request
        to Groq.
        """

        response = (
            self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
            )
        )

        return response.choices[0].message.content

    def extract_donation(
        self,
        email_body: str,
    ) -> dict:
        """
        Extract structured donation
        details from a restaurant email.
        """

        response = self._chat(
            prompt=DONATION_EXTRACTION_PROMPT,
            message=email_body,
            temperature=0,
        )

        return json.loads(response)

    def extract_need(
        self,
        email_body: str,
    ) -> dict:
        """
        Extract structured NGO need
        information.
        """

        response = self._chat(
            prompt=NEED_EXTRACTION_PROMPT,
            message=email_body,
            temperature=0,
        )

        return json.loads(response)

    def extract_ngo_reply(
        self,
        email_body: str,
    ) -> dict:
        """
        Extract NGO intent from
        an email reply.
        """

        response = self._chat(
            prompt=NGO_REPLY_PROMPT,
            message=email_body,
            temperature=0,
        )

        return json.loads(response)