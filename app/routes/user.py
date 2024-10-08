from fastapi import Request, APIRouter, Depends
from app.schema.user_schema import SignUpSchema, LoginSchema
from app.services.authentication_service import AuthenticationService
from app.core.jwt_manager import JWTManager
from app.core.custom_logger import logger

user_router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthenticationService()
jwt_manager = JWTManager()

@user_router.post("/signup/")
async def signup(request: Request, user_data: SignUpSchema):
    logger.info("Signup Request")
    return await auth_service.signup(user_data)

@user_router.post("/login/")
async def login(request: Request, user_data: LoginSchema):
    logger.info("Login Request")
    return await auth_service.login(user_data)

@user_router.post("/account_disable/")
async def account_disable(request: Request, password: str, current_user: str = Depends(jwt_manager.get_current_user)):
    logger.info("Account diable Request")
    return await auth_service.disable_account(current_user, password)

@user_router.post("/account_enable/")
async def account_enable(request: Request, user_data: LoginSchema):
    logger.info("Account enable Request")
    return await auth_service.enable_account(user_data)
