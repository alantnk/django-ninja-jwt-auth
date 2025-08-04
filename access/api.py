from ninja import Router, Schema
from ninja.errors import HttpError

from account.api import UserIn
from .services import token_service
from django.contrib.auth import authenticate

router = Router()


class TokenIn(Schema):
    token: str


@router.post("/token")
def token(request, body: UserIn) -> dict:

    user = authenticate(username=body.email, password=body.password)
    if not user:
        raise HttpError(401, "Invalid credentials")
    return token_service.retrieve_tokens(body.email)


@router.post("/refresh-token")
def refresh_token(request, body: TokenIn) -> dict:
    token = body.token

    try:
        new_access_token = token_service.refresh_token(token)
        return {"access_token": new_access_token}
    except Exception as e:
        return {"error": str(e)}, 400
