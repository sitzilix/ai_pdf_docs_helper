from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.token import Token

from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import EmailAlreadyExistsError


class AuthService:
    
    @staticmethod
    async def register(
        db: AsyncSession,
        user_data: UserCreate,
    ) -> User:
        
        query = select(User).where(
            User.email == user_data.email
        )
        
        result = await db.execute(query)
        
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise EmailAlreadyExistsError("User with this email already exists")
        
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )
        
        db.add(user)
        
        await db.commit()
        
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def auth_user(db: AsyncSession, email: str, password: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> Token:
        user = await AuthService.auth_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")