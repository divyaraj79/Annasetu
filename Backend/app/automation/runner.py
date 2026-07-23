import asyncio

from app.database import SessionLocal
from app.automation.scheduler import Scheduler


async def scheduler_loop():
    """
    Run the automation scheduler forever.
    """

    while True:
        db = SessionLocal()

        try:
            scheduler = Scheduler(db)
            scheduler.run_once()

        except Exception as e:
            print(f"[Scheduler] Error: {e}")

        finally:
            db.close()

        # Check Gmail every 30 seconds
        await asyncio.sleep(30)