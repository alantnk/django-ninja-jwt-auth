from ninja import NinjaAPI
from ninja.errors import HttpError
from accounts.auth import AuthBearer
from accounts.models import User
from accounts.api import UserIn


api = NinjaAPI()

api.add_router("auth/", "accounts.api.router")


@api.get("/protected", auth=AuthBearer())
def protected(request):
    return {"message": f"Hello, {request.auth}!"}


@api.post("/signup", response={201: dict, 400: dict})
def signup(request, body: UserIn) -> dict:
    user = User.objects.filter(username=body.username).exists()
    if not user:
        User.objects.create_user(
            username=body.username,
            password=body.password,
        )
        return 201, {"message": "User created successfully"}
    else:
        raise HttpError(400, "User already exists")
