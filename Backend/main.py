from fastapi import FastAPI

from app.routers.donation_router import router as donation_router
from app.routers.match_router import router as match_router
from app.routers.need_router import router as need_router
from app.routers.ngo_router import router as ngo_router
from app.routers.restaurant_router import router as restaurant_router
from app.routers.user_router import router as user_router

app = FastAPI(title="AnnaSetu API")

app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(ngo_router)
app.include_router(donation_router)
app.include_router(need_router)
app.include_router(match_router)


@app.get("/")
def root():
    return {"message": "AnnaSetu Backend Running 🚀"}