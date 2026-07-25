import asyncio

from app.database import SessionLocal
from app.automation.scheduler import Scheduler

# Testing interval
# SCHEDULER_INTERVAL = 600  # 10 minutes
SCHEDULER_INTERVAL = 160  # 2 min 40 seconds


async def scheduler_runner():

    while True:

        db = SessionLocal()

        try:
            print("Scheduler cycle started...")

            Scheduler(
                db,
            ).run_once()

        except Exception as exc:

            print(
                f"Scheduler Error: {exc}"
            )

        finally:

            db.close()

        await asyncio.sleep(
            SCHEDULER_INTERVAL
        )