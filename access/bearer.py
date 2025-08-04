from ninja.security import HttpBearer
from .services import token_service


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> str | None:
        """
        Authenticate the user using the provided token.
        """

        try:
            payload = token_service.decode_token(token)
            return payload.get("username")
        except Exception:
            return None
