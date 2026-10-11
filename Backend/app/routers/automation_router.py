from fastapi import APIRouter, Header, HTTPException, status

from app.database import SessionLocal
from app.automation.scheduler import Scheduler
from app.config import AUTOMATION_SECRET

router = APIRouter(
    prefix="/automation",
    tags=["automation"],
)


@router.post("/run")
def run_scheduler(
    authorization: str | None = Header(None),
):

    expected = f"Bearer {AUTOMATION_SECRET}"

    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    db = SessionLocal()

    try:
        Scheduler(db).run_once()
        db.commit()

        return {
            "message": "Automation completed successfully."
        }

    finally:
        db.close()