from fastapi import FastAPI
from app.core.config import settings

from app.api.health import router as health_router
from app.api.auth import router as auth_router

app = FastAPI(title="AI Engineer API")

app.include_router(health_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "AI Engineer API",
            "db_host": settings.DB_HOST,
            "db_name": settings.DB_NAME
            }