from ninja.security import HttpBearer
from .services import JWTService, JWTServiceProtocol


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> str | None:
        """
        Authenticate the user using the provided token.
        """
        jwt_service: JWTServiceProtocol = JWTService
        try:
            payload = jwt_service.decode_token(
                token, jwt_service.get_secret()
            )  # noqa: E501
            return payload.get("username")
        except Exception:
            return None
