from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Engineer API",
            "db_host": settings.DB_HOST,
            "db_name": settings.DB_NAME
            }