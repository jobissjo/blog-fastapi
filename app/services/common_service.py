import asyncio
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user_schema import UserTokenDecodedData
from app.core.settings import settings
from fastapi.exceptions import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


class CommonService:
    @staticmethod
    async def hash_password(password: str) -> str:
        def hashing(password: str) -> str:
            return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )

        return await asyncio.to_thread(hashing, password)

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool:
        def verify(password: str, hashed_password: str) -> bool:
            return bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )

        return await asyncio.to_thread(verify, password, hashed_password)

    @staticmethod
    async def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=1080))
        to_encode.update({"exp": expire, "token_type": "access"})
        return await asyncio.to_thread(
            jwt.encode, to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    async def create_refresh_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
        to_encode.update(
            {
                "exp": expire,
                "token_type": "refresh",  # you can differentiate token types if needed
            }
        )

        return await asyncio.to_thread(
            jwt.encode, to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    async def verify_refresh_token(token: str) -> dict:
        try:
            payload = await asyncio.to_thread(
                jwt.decode, token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            print(payload, "payload")
            if payload.get("token_type") != "refresh":
                raise HTTPException(detail="Invalid token type", status_code=401)
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise HTTPException(detail="Token is missing user id", status_code=401)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(detail="Token has expired", status_code=401)
        except jwt.PyJWTError as e:
            raise HTTPException(detail=f"Token is invalid: {e}", status_code=401)

    @staticmethod
    async def verify_token_get_user(
        token: str = Depends(oauth2_scheme),
    ) -> UserTokenDecodedData:
        try:
            payload = await asyncio.to_thread(
                jwt.decode, token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            print(payload, "payload")
            if payload.get("token_type") != "access":
                raise HTTPException(detail="Invalid token type", status_code=401)
            user_id: str = payload.get("id")
            if user_id is None:
                raise HTTPException(detail="Token is missing user id", status_code=401)
            return UserTokenDecodedData(**payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(detail="Token has expired", status_code=401)
        except jwt.PyJWTError as e:
            raise HTTPException(detail=f"Token is invalid: {e}", status_code=401)


    @staticmethod
    async def to_datetime(date_obj):
        if isinstance(date_obj, datetime):
            return date_obj
        elif hasattr(date_obj, "year"):
            return datetime(date_obj.year, date_obj.month, date_obj.day)
        return date_obj