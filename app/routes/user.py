from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema.user_schema import SignUpSchema, LoginSchema
from app.services.authentication_service import AuthenticationService
from app.core.jwt_manager import JWTManager
from app.core.custom_logger import logger
from app.db.base import get_db

user_router = APIRouter(prefix="/auth", tags=["Authentication"])
jwt_manager = JWTManager()

@user_router.post("/signup/")
async def signup(request: Request, user_data: SignUpSchema, db: Session=Depends(get_db)):
    auth_service = AuthenticationService(db)
    logger.info("Signup Request")
    return await auth_service.signup(user_data)

@user_router.post("/login/")
async def login(request: Request, user_data: LoginSchema, db: Session=Depends(get_db)):
    auth_service = AuthenticationService(db)
    logger.info("Login Request")
    return await auth_service.login(user_data)

@user_router.post("/account_disable/")
async def account_disable(request: Request, password: str, current_user: str = Depends(jwt_manager.get_current_user), db: Session=Depends(get_db)):
    auth_service = AuthenticationService(db)
    logger.info("Account diable Request")
    return await auth_service.disable_account(current_user, password)

@user_router.post("/account_enable/")
async def account_enable(request: Request, user_data: LoginSchema, db: Session=Depends(get_db)):
    auth_service = AuthenticationService(db)
    logger.info("Account enable Request")
    return await auth_service.enable_account(user_data)
