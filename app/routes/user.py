from fastapi import Request, APIRouter, Response
from app.schema.user_schema import SignUpSchema
from app.services.authentication_service import AuthenticationService

user_router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthenticationService()


@user_router.post("/signup/")
async def signup(request: Request, user_data: SignUpSchema):
    return await auth_service.signup(user_data)
