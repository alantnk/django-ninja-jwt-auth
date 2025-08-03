from ninja import Router, Schema
from ninja.errors import HttpError
from .services import JWTService
from django.contrib.auth import authenticate

router = Router()


class UserIn(Schema):
    username: str
    password: str


class TokenIn(Schema):
    token: str


@router.post("/token")
def token(request, body: UserIn) -> dict:

    user = authenticate(username=body.username, password=body.password)
    if not user:
        raise HttpError(401, "Invalid credentials")
    return JWTService.retrieve_tokens(body.username)


@router.post("/refresh-token")
def refresh_token(request, body: TokenIn) -> dict:
    token = body.token

    try:
        new_access_token = JWTService.refresh_access_token(token)
        return {"access_token": new_access_token}
    except Exception as e:
        return {"error": str(e)}, 400
