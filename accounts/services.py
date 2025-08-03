import jwt
from datetime import datetime, timedelta, timezone
from typing import Protocol
from decouple import config

JWT_SECRET = config("JWT_SECRET")


class JWTServiceProtocol(Protocol):

    def get_secret(cls) -> str:
        pass

    def retrieve_tokens(cls, username: str) -> dict:
        pass

    def encode_token(cls, payload: dict, secret: str, exp: timedelta) -> str:
        pass

    def decode_token(cls, token: str, secret: str) -> dict:
        pass

    def verify_token(cls, token: str, secret: str) -> bool:
        pass

    def refresh_access_token(cls, refresh_token: str) -> str:
        pass


class JWTService:
    _REF_KEY_PREFIX = "refresh_"
    _ALGORITHM = "HS256"
    _SECRET = JWT_SECRET

    @classmethod
    def get_secret(cls) -> str:
        secret = cls._SECRET.strip()
        return secret.strip()

    @classmethod
    def retrieve_tokens(cls, username: str) -> dict:
        access_token = cls.encode_token(
            {"username": username},
            cls.get_secret(),
            timedelta(minutes=5),
        )

        refresh_token = cls.encode_token(
            {"username": username},
            cls._REF_KEY_PREFIX + cls.get_secret(),
            timedelta(days=7),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @classmethod
    def encode_token(cls, payload: dict, secret: str, exp: timedelta) -> str:
        return jwt.encode(
            {**payload, "exp": datetime.now(tz=timezone.utc) + exp},
            secret,
            algorithm=cls._ALGORITHM,
        )

    @classmethod
    def decode_token(cls, token: str, secret: str) -> dict:
        return jwt.decode(
            token,
            secret,
            algorithms=[cls._ALGORITHM],
        )

    @classmethod
    def verify_token(cls, token: str, secret: str) -> bool:
        try:
            cls.decode_token(token, secret)
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        try:
            payload = cls.decode_token(
                refresh_token, cls._REF_KEY_PREFIX + cls.get_secret()
            )  # noqa: E501
            return cls.encode_token(
                {"username": payload["username"]},
                cls.get_secret(),
                timedelta(minutes=5),
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token.")
