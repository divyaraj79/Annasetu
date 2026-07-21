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

app = FastAPI(title="AnnaSetu API")

register_exception_handlers(app)
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