from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.config import settings

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router

from app.core.exceptions import EmailAlreadyExistsError

app = FastAPI(title="AI Engineer API")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "AI Engineer API",
            "db_host": settings.DB_HOST,
            "db_name": settings.DB_NAME
            }
    
@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User with this email already exists"},
    )