from fastapi import FastAPI

from app.routers.donation_router import router as donation_router
from app.routers.match_router import router as match_router
from app.routers.need_router import router as need_router
from app.routers.ngo_router import router as ngo_router
from app.routers.restaurant_router import router as restaurant_router
from app.routers.user_router import router as user_router
from app.routers.donation_item_router import router as donation_item_router
from app.routers.auth_router import router as auth_router
from app.core.exception_handler import register_exception_handlers
from app.routers.admin_router import router as admin_router
from app.routers.automation_router import (
    router as automation_router,
)

# from contextlib import asynccontextmanager
# import asyncio

# from app.automation.runner import scheduler_runner 

# @asynccontextmanager
# async def lifespan(app: FastAPI):

#     task = asyncio.create_task(
#         scheduler_runner()
#     )

#     try:
#         yield
#     finally:
#         task.cancel()

#         try:
#             await task
#         except asyncio.CancelledError:
#             pass


# app = FastAPI(
#     title="AnnaSetu API",
#     lifespan=lifespan,
# )

app = FastAPI(
    title="AnnaSetu API",
)

register_exception_handlers(app)
app.include_router(automation_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(restaurant_router)
app.include_router(ngo_router)
app.include_router(donation_router)
app.include_router(donation_item_router)
app.include_router(need_router)
app.include_router(match_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "AnnaSetu Backend Running 🚀"}