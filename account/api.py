from pydantic import EmailStr, Field
from django.contrib.auth import get_user_model
from django.db.models import Q
from ninja import Router, Schema
from ninja.errors import HttpError
from account.models import Profile
from django.db import transaction

User = get_user_model()

router = Router()


class UserIn(Schema):
    email: EmailStr
    password: str = Field(min_length=6)


@router.post("/signup", response={201: dict, 400: dict})
def signup(request, data: UserIn) -> dict:
    user = User.objects.filter(Q(email=data.email)).exists()  # noqa: E501
    if not user:
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=data.email,
                    email=data.email,
                    password=data.password,
                )

                Profile.objects.create(user=new_user)

                return 201, {"message": "Account created successfully"}
        except Exception:
            raise HttpError(400, "Error creating account")
    else:
        raise HttpError(400, "User already exists")
