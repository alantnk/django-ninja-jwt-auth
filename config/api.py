from ninja import NinjaAPI

from access.bearer import AuthBearer

api = NinjaAPI()

api.add_router("auth/", "access.api.router")
api.add_router("account/", "account.api.router")


@api.get("/protected", auth=AuthBearer())
def protected(request):
    return {"message": f"Hello, {request.auth}!"}
