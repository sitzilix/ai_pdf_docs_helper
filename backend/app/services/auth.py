from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import hash_password
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