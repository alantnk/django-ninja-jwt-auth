import jwt
from datetime import datetime, timedelta, timezone
from decouple import config

JWT_SECRET = config("JWT_SECRET")


class JWTService:
    _REF_KEY_PREFIX = "refresh_"
    _ALGORITHM = "HS256"
    _SECRET = JWT_SECRET

    def _get_secret(self) -> str:
        secret = self._SECRET.strip()
        return secret.strip()

    def retrieve_tokens(self, username: str) -> dict:
        access_token = self._encode(
            {"username": username},
            self._get_secret(),
            timedelta(minutes=5),
        )

        refresh_token = self._encode(
            {"username": username},
            self._REF_KEY_PREFIX + self._get_secret(),
            timedelta(days=7),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def _encode(self, payload: dict, secret: str, exp: timedelta) -> str:
        return jwt.encode(
            {**payload, "exp": datetime.now(tz=timezone.utc) + exp},
            secret,
            algorithm=self._ALGORITHM,
        )

    def _decode(self, token: str, secret: str) -> dict:
        return jwt.decode(
            token,
            secret,
            algorithms=[self._ALGORITHM],
        )

    def decode_token(self, token: str) -> dict:
        return self._decode(token, self._get_secret())

    def verify_token(self, token: str, secret: str) -> bool:
        try:
            self._decode(token, secret)
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = self._decode(
                refresh_token, self._REF_KEY_PREFIX + self._get_secret()
            )  # noqa: E501
            return self._encode(
                {"username": payload["username"]},
                self._get_secret(),
                timedelta(minutes=5),
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token.")


token_service = JWTService()

"__all__" == [
    "token_service",
]
