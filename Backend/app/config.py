from dotenv import load_dotenv
import os

from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_PATH = Path(
    os.getenv(
        "GMAIL_CREDENTIALS_PATH",
        str(BASE_DIR / "credentials.json"),
    )
)

TOKEN_PATH = Path(
    os.getenv(
        "GMAIL_TOKEN_PATH",
        str(BASE_DIR / "token.json"),
    )
)



def get_required_env(variable_name: str) -> str:
    value = os.getenv(variable_name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {variable_name}"
        )

    return value


DATABASE_URL = get_required_env("DATABASE_URL")

SECRET_KEY = get_required_env("SECRET_KEY")

AUTOMATION_SECRET = get_required_env(
    "AUTOMATION_SECRET"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256",
)

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30",
        )
    )

    if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
        raise ValueError

except ValueError:
    raise RuntimeError(
        "ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer."
    )