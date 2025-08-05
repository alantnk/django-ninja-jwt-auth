from ninja import Router, Schema
from ninja.errors import HttpError

from account.api import UserIn
from .services import token_service
from django.contrib.auth import authenticate

router = Router()


class TokenIn(Schema):
    token: str


class TokenOut(Schema):
    access_token: str


@router.post("/token")
def token(request, data: UserIn):

    user = authenticate(username=data.email, password=data.password)
    if not user:
        raise HttpError(401, "Invalid credentials")
    return token_service.retrieve_tokens(data.email)


@router.post("/refresh-token", response={200: TokenOut, 400: dict})
def refresh_token(request, data: TokenIn):
    token = data.token

    try:
        new_access_token = token_service.refresh_token(token)
        return {"access_token": new_access_token}
    except Exception as e:
        raise HttpError(400, str(e))
