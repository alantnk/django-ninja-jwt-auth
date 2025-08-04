from pydantic import EmailStr
from django.contrib.auth import get_user_model
from django.db.models import Q
from ninja import Router, Schema
from ninja.errors import HttpError

User = get_user_model()

router = Router()


class UserIn(Schema):
    email: EmailStr
    password: str


@router.post("/signup", response={201: dict, 400: dict})
def signup(request, body: UserIn) -> dict:
    user = User.objects.filter(Q(email=body.email)).exists()  # noqa: E501
    if not user:
        User.objects.create_user(
            username=body.email,
            email=body.email,
            password=body.password,
        )
        return 201, {"message": "User created successfully"}
    else:
        raise HttpError(400, "User already exists")
